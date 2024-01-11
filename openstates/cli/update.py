# ruff: noqa: E402

from openstates.utils.django import init_django

init_django()

import argparse
import contextlib
import datetime
import glob
import importlib
import logging
import os
import signal
import sys
import traceback
import typing
from types import ModuleType

from django.db import transaction
from openstates import settings, utils
from openstates.civiqa import civiqa_env
from openstates.civiqa.publisher import publish_os_update_finished
from openstates.cli.reports import (
    ImportReport,
    Plan,
    Report,
    ScraperReport,
    generate_session_data_quality_report,
    print_report,
    save_report,
)
from openstates.data.models import Jurisdiction, LegislativeSession, RunPlan
from openstates.exceptions import CommandError, ScrapeError
from openstates.importers import (
    BillImporter,
    EventImporter,
    JurisdictionImporter,
    VoteEventImporter,
)
from openstates.importers.base import BaseImporter
from openstates.scrape import JurisdictionScraper, State
from openstates.scrape.base import Scraper

logger = logging.getLogger("openstates")


ALL_ACTIONS = ("scrape", "import")


class _Unset:
    pass


UNSET = _Unset()


@contextlib.contextmanager
def override_settings(settings, overrides):  # type: ignore
    original = {}
    for key, value in overrides.items():
        original[key] = getattr(settings, key, UNSET)
        setattr(settings, key, value)
    yield
    for key, value in original.items():
        if value is UNSET:
            delattr(settings, key)
        else:
            setattr(settings, key, value)


def get_jurisdiction(module_name: str) -> tuple[State, ModuleType]:
    # get the state object
    module = importlib.import_module(module_name)
    for obj in module.__dict__.values():
        # ensure we're dealing with a subclass of State
        if isinstance(obj, type) and issubclass(obj, State) and obj != State:
            return obj(), module
    raise CommandError(f"Unable to import State subclass from {module_name}")


def do_scrape(
    state: State,
    legislative_session: LegislativeSession,
    args: argparse.Namespace,
    scraper_args_by_name: dict[str, dict[str, str]],
    bill_scrape_reports: dict[str, ScraperReport] = {},
) -> dict[str, ScraperReport]:

    scraper_reports: dict[str, ScraperReport] = {}

    for scraper_name, scraper_args in scraper_args_by_name.items():
        # make output and cache dirs
        utils.makedirs(settings.CACHE_DIR)
        datadir = os.path.join(settings.SCRAPED_DATA_DIR, args.module, scraper_name)
        utils.makedirs(datadir)
        # clear json from data dir
        for f in glob.glob(datadir + "/*.json"):
            os.remove(f)

        ScraperClass = state.scrapers[scraper_name]
        # new scraper each time
        scraper: Scraper = ScraperClass(
            state,
            datadir,
            legislative_session=legislative_session,
            strict_validation=args.strict,
            fastmode=args.fastmode,
            realtime=args.realtime,
        )
        # votes scrapers depend on a successful bills scrape
        if scraper_name == "votes":
            bill_scrape_report = bill_scrape_reports.get(legislative_session.id)
            if bill_scrape_report is None or bill_scrape_report.end is None:
                raise ScrapeError(
                    f"Votes scraper requires successful bills scrape run for {legislative_session.identifier}"
                )

        scraper_reports[scraper_name] = scraper.do_scrape(**scraper_args)

    return scraper_reports


def do_import(
    state: State, from_scrapers: list[str], args: argparse.Namespace
) -> dict[str, typing.Any]:
    jurisdiction_importer = JurisdictionImporter(state.jurisdiction_id)
    bill_importer = BillImporter(state.jurisdiction_id)
    vote_event_importer = VoteEventImporter(state.jurisdiction_id, bill_importer)
    event_importer = EventImporter(state.jurisdiction_id, vote_event_importer)

    importers_per_scraper: dict[str, list[BaseImporter]] = {
        "jurisdiction": [jurisdiction_importer],
        "bills": [bill_importer, vote_event_importer],
        "events": [event_importer],
        "votes": [vote_event_importer],
    }
    
    importers: dict[BaseImporter, str] = {}
    for scraper in from_scrapers:
        for importer in importers_per_scraper[scraper]:
            importers[importer] = scraper

    import_reports: dict[str, ImportReport] = {}

    def do_importer(importer: BaseImporter, scraper_name: str) -> None:
        datadir = os.path.join(settings.SCRAPED_DATA_DIR, args.module, scraper_name)
        import_type = importer._type
        logger.info(f"import {import_type}s...")
        import_report = importer.import_directory(datadir)
        import_reports[import_type] = import_report

    with transaction.atomic():
        for importer, scraper_name in importers.items():
            do_importer(importer, scraper_name)

        Jurisdiction.objects.filter(id=state.jurisdiction_id).update(
            latest_bill_update=datetime.datetime.utcnow()
        )

    return import_reports


def check_session_list(juris: State) -> set[str]:
    scraper = type(juris).__name__

    # if get_session_list is not defined
    if not hasattr(juris, "get_session_list"):
        raise CommandError(f"{scraper}.get_session_list() is not provided")

    scraped_sessions = juris.get_session_list()

    if not scraped_sessions:
        raise CommandError("no sessions from {}.get_session_list()".format(scraper))

    active_sessions = set()
    # copy the list to avoid modifying it
    sessions = set(juris.ignored_scraped_sessions)
    for session in juris.legislative_sessions:
        sessions.add(session.get("_scraped_name", session["identifier"]))
        if session.get("active"):
            active_sessions.add(session.get("identifier"))

    if not active_sessions:
        raise CommandError(f"No active sessions on {scraper}")

    unaccounted_sessions = list(set(scraped_sessions) - sessions)
    if unaccounted_sessions:
        raise CommandError(
            (
                "Session(s) {sessions} were reported by {scraper}.get_session_list() "
                "but were not found in {scraper}.legislative_sessions or "
                "{scraper}.ignored_scraped_sessions."
            ).format(sessions=", ".join(unaccounted_sessions), scraper=scraper)
        )
    return active_sessions


def do_update(
    args: argparse.Namespace,
    other_args: list[str],
    state: State,
) -> list[RunPlan]:
    available_scrapers = getattr(state, "scrapers", {})
    scraper_args_by_name: dict[str, dict[str, str]] = {}

    if not available_scrapers:
        raise CommandError("no scrapers defined on jurisdiction")

    available_scrapers["jurisdiction"] = JurisdictionScraper
    scrapers_to_run: list[str] = []
    scraper_args_by_name = {}
    if other_args:
        # if the cmd line specified scrapers, only run those
        scraper_args_by_name = _get_custom_scraper_args(
            other_args, available_scrapers, args
        )
        scrapers_to_run = list(scraper_args_by_name.keys())
    else:
        scrapers_to_run = list(available_scrapers.keys())

    order = ["jurisdiction", "bills", "votes", "events"]
    scrapers_to_run.sort(key=lambda s: order.index(s) if s in order else 999)

    # modify args in-place so we can pass them around
    if not args.actions:
        args.actions = ALL_ACTIONS

    run_plan_models: list[RunPlan] = []
    bill_scrape_reports: dict[str, ScraperReport] = {}

    for scraper_name in scrapers_to_run:
        scraper_args = scraper_args_by_name.get(scraper_name, {})

        legislative_sessions: list[LegislativeSession]
        if scraper_name != "jurisdiction":
            legislative_sessions = get_legislative_sessions(args, state)
        else:
            legislative_sessions = [None]

        for legislative_session in legislative_sessions:
            report = Report(
                jurisdiction_id=state.jurisdiction_id,
                legislative_session=legislative_session,
                start=utils.utcnow(),
                plan=Plan(
                    module=args.module,
                    actions=args.actions,
                    scraper_args_by_name={scraper_name: scraper_args},
                ),
            )

            _print_report(report, "Initial report")

            # save the pending report
            run_plan_model = save_report(report)
            try:
                if "scrape" in args.actions:
                    report.scraper_reports = do_scrape(
                        state,
                        legislative_session,
                        args,
                        report.plan.scraper_args_by_name,
                    )
                    if "bills" in report.scraper_reports:
                        bill_scrape_reports[
                            legislative_session.id
                        ] = report.scraper_reports["bills"]

                if "import" in args.actions:
                    scraper_names = list(report.scraper_reports.keys())
                    report.import_reports = do_import(state, scraper_names, args)

                report.success = True
            except Exception as exc:
                report.success = False
                report.exception = exc
                report.traceback = traceback.format_exc()

            report.end = utils.utcnow()
            run_plan_model = save_report(report, run_plan_model)
            run_plan_models.append(run_plan_model)

            if legislative_session:
                has_votes_scraper = state.scrapers.get("votes") is not None
                _set_attempted_scrape_at(legislative_session, scraper_name, report.start)
                if scraper_name == "bills" and not has_votes_scraper:
                    _set_attempted_scrape_at(legislative_session, "votes", report.start)

                if report.success:
                    _set_successful_scrape_at(legislative_session, scraper_name, report.end)
                    if scraper_name == "bills" and not has_votes_scraper:
                        _set_successful_scrape_at(legislative_session, "votes", report.end)

                legislative_session.save()

            if report.success:
                if scraper_name in ("bills", "votes"):
                    generate_session_data_quality_report(
                        legislative_session=report.legislative_session,
                        run_plan=run_plan_model,
                    )

            publish_os_update_finished(run_plan_model)
            _print_report(report, "Final report")

    return run_plan_models


def _set_attempted_scrape_at(
    legislative_session: LegislativeSession,
    scraper_name: str,
    start: datetime.datetime,
) -> None:
    attr = f"last_attempted_{scraper_name}_scrape_at"
    if hasattr(legislative_session, attr):
        setattr(legislative_session, attr, start)
        legislative_session.save()


def _set_successful_scrape_at(
    legislative_session: LegislativeSession,
    scraper_name: str,
    end: datetime.datetime,
) -> None:
    attr = f"last_successful_{scraper_name}_scrape_at"
    if hasattr(legislative_session, attr):
        setattr(legislative_session, attr, end)
        legislative_session.save()


def _print_report(report: Report, caption: str) -> None:
    print()
    print()
    print(f"### {caption}")
    print()
    print_report(report)
    print()


def _get_custom_scraper_args(
    other_args: list[str], available_scrapers: dict[str, type], args: argparse.Namespace
) -> dict[str, dict[str, str]]:
    result = {}
    # parse arg list in format: (scraper (k=v )+)+
    scraper_name = None
    for arg in other_args:
        if "=" in arg:
            if not scraper_name:
                raise CommandError("argument {} before scraper name".format(arg))
            k, v = arg.split("=", 1)
            v = v.strip("'")
            result[scraper_name][k] = v
        elif arg in available_scrapers:
            scraper_name = arg
            result[scraper_name] = {}
        else:
            raise CommandError(
                "no such scraper: module={} scraper={}".format(args.module, arg)
            )
    return result


def get_legislative_sessions(args: argparse.Namespace, state: State) -> None:
    legislative_sessions = []
    if args.session:
        legislative_sessions = LegislativeSession.objects.filter(
            identifier=args.session.strip("'"),
            jurisdiction_id=state.jurisdiction_id,
        )
        if not legislative_sessions:
            raise CommandError(
                f"session {args.session} not found in {state.jurisdiction_id}"
            )
    else:
        active_sessions = check_session_list(state)
        logger.info(
            f"no session specified. scraping all active sessions: {active_sessions}"
        )
        legislative_sessions = LegislativeSession.objects.filter(
            identifier__in=active_sessions, jurisdiction_id=state.jurisdiction_id
        )
        if not legislative_sessions:
            raise CommandError("no active legislative sessions found")
    return legislative_sessions


def parse_args() -> tuple[argparse.Namespace, list[str]]:
    parser = argparse.ArgumentParser("openstates", description="openstates CLI")
    parser.add_argument("--debug", action="store_true", help="open debugger on error")
    parser.add_argument(
        "--loglevel",
        default="INFO",
        help=(
            "set log level. options are: "
            "DEBUG|INFO|WARNING|ERROR|CRITICAL "
            "(default is INFO)"
        ),
    )

    # what to scrape
    parser.add_argument("module", type=str, help="path to scraper module")
    parser.add_argument("--session", type=str, help="session to scrape")

    for arg in ALL_ACTIONS:
        parser.add_argument(
            "--" + arg,
            dest="actions",
            action="append_const",
            const=arg,
            help="only run {} post-scrape step".format(arg),
        )

    # scraper arguments
    parser.add_argument(
        "--nonstrict",
        action="store_false",
        dest="strict",
        help="skip validation on save",
    )
    parser.add_argument(
        "--fastmode", action="store_true", help="use cache and turn off throttling"
    )

    # settings overrides
    parser.add_argument("--datadir", help="data directory", dest="SCRAPED_DATA_DIR")
    parser.add_argument("--cachedir", help="cache directory", dest="CACHE_DIR")
    parser.add_argument(
        "-r", "--rpm", help="scraper rpm", type=int, dest="SCRAPELIB_RPM"
    )
    parser.add_argument(
        "--timeout", help="scraper timeout", type=int, dest="SCRAPELIB_TIMEOUT"
    )
    parser.add_argument(
        "--no-verify",
        help="skip tls verification",
        action="store_false",
        dest="SCRAPELIB_VERIFY",
    )
    parser.add_argument(
        "--retries", help="scraper retries", type=int, dest="SCRAPELIB_RETRIES"
    )
    parser.add_argument(
        "--retry_wait",
        help="scraper retry wait",
        type=int,
        dest="SCRAPELIB_RETRY_WAIT_SECONDS",
    )

    # realtime mode
    parser.add_argument("--realtime", action="store_true", help="enable realtime mode")

    # process args
    return parser.parse_known_args()


def main() -> int:
    args, other = parse_args()

    civiqa_env.load()

    # set log level from command line
    handler_level = getattr(logging, args.loglevel.upper(), "INFO")
    settings.LOGGING["handlers"]["default"]["level"] = handler_level  # type: ignore
    logging.config.dictConfig(settings.LOGGING)

    if args.debug:
        try:
            debug_module = importlib.import_module("ipdb")
        except ImportError:
            debug_module = importlib.import_module("pdb")

        # turn on PDB-on-error mode
        # stolen from http://stackoverflow.com/questions/1237379/
        # if this causes problems in interactive mode check that page
        def _tb_info(type, value, tb):  # type: ignore
            traceback.print_exception(type, value, tb)
            debug_module.pm()

        sys.excepthook = _tb_info

    logging.info(f"Module: {args.module}")

    juris, module = get_jurisdiction(args.module)

    overrides = {}
    overrides.update(getattr(module, "settings", {}))
    overrides.update(
        {key: value for key, value in vars(args).items() if value is not None}
    )
    with override_settings(settings, overrides):
        report = do_update(args, other, juris)

    if any(not r.success for r in report):
        return 1
    else:
        return 0


def shutdown_handler(signal: int, _) -> None:
    logger.info("Signal received, safely shutting down.")
    print("Exiting process.", flush=True)
    sys.exit(0)


if __name__ == "__main__":
    signal.signal(signal.SIGINT, shutdown_handler)
    sys.exit(main())
