# ruff: noqa: E402

from openstates.utils.django import init_django

init_django()

import argparse
import contextlib
import datetime
import glob
import importlib
import inspect
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
from openstates.exceptions import CommandError
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
) -> dict[str, ScraperReport]:
    # make output and cache dirs
    utils.makedirs(settings.CACHE_DIR)
    datadir = os.path.join(settings.SCRAPED_DATA_DIR, args.module)
    utils.makedirs(datadir)
    # clear json from data dir
    for f in glob.glob(datadir + "/*.json"):
        os.remove(f)

    scraper_reports: dict[str, ScraperReport] = {}

    # do jurisdiction
    jurisdiction_scraper = JurisdictionScraper(
        state,
        datadir,
        strict_validation=args.strict,
        fastmode=args.fastmode,
        realtime=args.realtime,
    )
    scraper_reports["jurisdiction"] = jurisdiction_scraper.do_scrape()

    for scraper_name, scraper_args in scraper_args_by_name.items():
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

        if (
            "session" in inspect.getargspec(ScraperClass.scrape).args
            and "session" not in scraper_args
        ):
            scraper_args["session"] = legislative_session.identifier

        scraper_reports[scraper_name] = scraper.do_scrape(**scraper_args)

    return scraper_reports


def do_import(state: State, args: argparse.Namespace) -> dict[str, typing.Any]:
    datadir = os.path.join(settings.SCRAPED_DATA_DIR, args.module)

    jurisdiction_importer = JurisdictionImporter(state.jurisdiction_id)
    bill_importer = BillImporter(state.jurisdiction_id)
    vote_event_importer = VoteEventImporter(state.jurisdiction_id, bill_importer)
    event_importer = EventImporter(state.jurisdiction_id, vote_event_importer)

    importers: list[BaseImporter] = [
        bill_importer,
        vote_event_importer,
        event_importer,
    ]

    import_reports: dict[str, ImportReport] = {}

    def do_importer(importer: BaseImporter) -> None:
        import_type = importer._type
        logger.info(f"import {import_type}s...")
        import_report = importer.import_directory(datadir)
        import_reports[import_type] = import_report

    # do jurisdiction first
    do_importer(jurisdiction_importer)

    with transaction.atomic():
        for importer in importers:
            do_importer(importer)

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
    default_scrapers = getattr(state, "default_scrapers", None)
    scraper_args_by_name: dict[str, dict[str, str]] = {}

    if not available_scrapers:
        raise CommandError("no scrapers defined on jurisdiction")

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

    scraper_args_by_name = {}
    if other_args:
        # parse arg list in format: (scraper (k=v)+)+
        scraper_name = None
        for arg in other_args:
            if "=" in arg:
                if not scraper_name:
                    raise CommandError("argument {} before scraper name".format(arg))
                k, v = arg.split("=", 1)
                v = v.strip("'")
                scraper_args_by_name[scraper_name][k] = v
            elif arg in state.scrapers:
                scraper_name = arg
                scraper_args_by_name[scraper_name] = {}
            else:
                raise CommandError(
                    "no such scraper: module={} scraper={}".format(args.module, arg)
                )

    runs = []    
    if scraper_args_by_name:
        # if the cmd line specified scrapers, only run those
        runs = [list(scraper_args_by_name.keys())]
    else:
        scraper_args_by_name = {scraper_name: {} for scraper_name in available_scrapers}
        # prefer default_scrapers as they're own run
        if default_scrapers:
            runs = [default_scrapers]
            rest = []
            for scraper_name in available_scrapers:
                if scraper_name not in default_scrapers:
                    rest.append(scraper_name)
            if rest:
                runs.append(rest)
        else:
            runs = [list(available_scrapers.keys())]

    # modify args in-place so we can pass them around
    if not args.actions:
        args.actions = ALL_ACTIONS

    run_plan_models: list[RunPlan] = []
    for run in runs:
        run_scraper_args_by_name = {
            scraper_name: scraper_args_by_name[scraper_name] for scraper_name in run
        }
        for legislative_session in legislative_sessions:
            report = Report(
                jurisdiction_id=state.jurisdiction_id,
                legislative_session=legislative_session,
                start=utils.utcnow(),
                plan=Plan(
                    module=args.module,
                    actions=args.actions,
                    scraper_args_by_name=run_scraper_args_by_name,
                ),
            )
            print_report(report)

            try:
                if "scrape" in args.actions:
                    report.scraper_reports = do_scrape(
                        state, legislative_session, args, report.plan.scraper_args_by_name
                    )

                if "import" in args.actions:
                    report.import_reports = do_import(state, args)

                report.success = True
            except Exception as exc:
                report.success = False
                report.exception = exc
                report.traceback = traceback.format_exc()

            run_plan_model = save_report(report)
            run_plan_models.append(run_plan_model)

            if report.success:
                generate_session_data_quality_report(
                    legislative_session=report.legislative_session,
                    run_plan=run_plan_model,
                )
                publish_os_update_finished(run_plan_model)

            print_report(report)

    return run_plan_models


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
