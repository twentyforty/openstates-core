import datetime
from typing import Optional
import logging
from attr import dataclass
from django.db import transaction
from django.db.models import Count, Model, Subquery, OuterRef, Q, F

from openstates.data.models import (
    LegislativeSession,
    RunPlan,
    ScrapeObjects,
    ScrapeReport,
    Bill,
    VoteEvent,
    VoteCount,
    PersonVote,
    BillSponsorship,
    SessionDataQualityReport,
)
from openstates.data.models.reports import ImportObjects


from .. import utils

# model imports are inside functions since this file is imported pre-init

logger = logging.getLogger("openstates")


@dataclass
class ImportReport:
    insert: int
    update: int
    noop: int
    start: datetime.datetime
    records: dict[str, list[str]] = {}
    end: Optional[datetime.datetime] = None


@dataclass
class ScraperReport:
    start: datetime.datetime
    objects: dict[str, int]
    skipped: Optional[int] = None
    end: Optional[datetime.datetime] = None


@dataclass
class Plan:
    module: str
    actions: list[str]
    scraper_args_by_name: dict[str, dict[str, str]]


@dataclass
class Report:
    jurisdiction_id: str
    legislative_session: LegislativeSession
    plan: Plan
    start: datetime.datetime
    exception: str = ""
    traceback: str = ""
    end: Optional[datetime.datetime] = None
    success: bool = False
    scraper_reports: dict[str, ScraperReport] = {}
    import_reports: dict[str, ImportReport] = {}


def print_report(report: Report) -> None:
    plan = report.plan
    print("{} ({})".format(plan.module, ", ".join(plan.actions)))
    for scraper_name, args in plan.scraper_args_by_name.items():
        print("  {}: {}".format(scraper_name, args))
    if report.scraper_reports:
        for type, scrape_report in sorted(report.scraper_reports.items()):
            print(type + " scrape:")
            print("  duration: ", (scrape_report.end - scrape_report.start))
            print("  objects:")
            for object_type, count in sorted(scrape_report.objects.items()):
                print("    {}: {}".format(object_type, count))
    if report.import_reports:
        print("import:")
        for type, import_report in sorted(report.import_reports.items()):
            if import_report.insert or import_report.update or import_report.noop:
                print(
                    "  {}: {} new {} updated {} noop".format(
                        type,
                        import_report.insert,
                        import_report.update,
                        import_report.noop,
                    )
                )


@transaction.atomic
def save_report(report: Report) -> RunPlan:
    report.end = utils.utcnow()

    run_plan_model = RunPlan.objects.create(
        jurisdiction_id=report.jurisdiction_id,
        legislative_session=report.legislative_session,
        success=report.success,
        start_time=report.start,
        end_time=report.end,
        exception=report.exception,
        traceback=report.traceback,
    )

    for scraper_name, scrape_report in report.scraper_reports.items():
        scraper_args = ""
        for arg, value in report.plan.scraper_args_by_name.get(
            scraper_name, {}
        ).items():
            if " " in value:
                value = f"'{value}'"
            scraper_args += f"{arg}={value} "

        scrape_report_model = ScrapeReport.objects.create(
            plan=run_plan_model,
            scraper=scraper_name,
            legislative_session=report.legislative_session,
            args=scraper_args,
            start_time=scrape_report.start,
            end_time=scrape_report.end,
        )

        for object_type, count in scrape_report.objects.items():
            ScrapeObjects.objects.create(
                report=scrape_report_model, object_type=object_type, count=count
            )

    for importer_type, import_report in report.import_reports.items():
        if import_report.insert or import_report.update or import_report.noop:
            ImportObjects.objects.create(
                plan=run_plan_model,
                object_type=importer_type,
                insert_count=import_report.insert,
                update_count=import_report.update,
                noop_count=import_report.noop,
                start_time=import_report.start,
                end_time=import_report.end,
                records=import_report.records,
            )

    return run_plan_model


def _simple_count(
    ModelClass: Model, legislatve_session: LegislativeSession, **filter
) -> int:
    return (
        ModelClass.objects.filter(legislative_session=legislatve_session)
        .filter(**filter)
        .count()
    )


def generate_session_data_quality_report(
    legislative_session: LegislativeSession, run_plan: RunPlan = None
) -> SessionDataQualityReport:
    report = SessionDataQualityReport(
        legislative_session=legislative_session,
        run_plan=run_plan,
    )

    report.bills_missing_actions = _simple_count(
        Bill, legislative_session, actions__isnull=True
    )
    report.bills_missing_sponsors = _simple_count(
        Bill, legislative_session, sponsorships__isnull=True
    )
    report.bills_missing_versions = _simple_count(
        Bill, legislative_session, versions__isnull=True
    )
    report.votes_missing_bill = _simple_count(
        VoteEvent, legislative_session, bill__isnull=True
    )
    report.votes_missing_voters = _simple_count(
        VoteEvent, legislative_session, votes__isnull=True
    )
    report.votes_missing_yes_count = 0
    report.votes_missing_no_count = 0
    report.votes_with_bad_counts = 0

    voteevents = VoteEvent.objects.filter(legislative_session=legislative_session)
    # explicitly remove ordering pre-Django 3.1
    queryset = voteevents.order_by().annotate(
        yes_sum=Count("pk", filter=Q(votes__option="yes")),
        no_sum=Count("pk", filter=Q(votes__option="no")),
        other_sum=Count("pk", filter=Q(votes__option="other")),
        yes_count=Subquery(
            VoteCount.objects.filter(vote_event=OuterRef("pk"), option="yes").values(
                "value"
            )
        ),
        no_count=Subquery(
            VoteCount.objects.filter(vote_event=OuterRef("pk"), option="no").values(
                "value"
            )
        ),
        other_count=Subquery(
            VoteCount.objects.filter(vote_event=OuterRef("pk"), option="other").values(
                "value"
            )
        ),
    )

    for vote in queryset:
        if vote.yes_count is None:
            report.votes_missing_yes_count += 1
            vote.yes_count = 0
        if vote.no_count is None:
            report.votes_missing_no_count += 1
            vote.no_count = 0
        if vote.other_count is None:
            vote.other_count = 0
        if (
            vote.yes_sum != vote.yes_count
            or vote.no_sum != vote.no_count
            or vote.other_sum != vote.other_count
        ):
            report.votes_with_bad_counts += 1

    # handle unmatched
    queryset = (
        BillSponsorship.objects.filter(
            bill__legislative_session=legislative_session,
            entity_type="person",
            person_id=None,
        )
        .values("name")
        .annotate(num=Count("name"))
    )
    report.unmatched_sponsor_people = {item["name"]: item["num"] for item in queryset}
    queryset = (
        BillSponsorship.objects.filter(
            bill__legislative_session=legislative_session,
            entity_type="organization",
            person_id=None,
        )
        .values("name")
        .annotate(num=Count("name"))
    )
    report.unmatched_sponsor_organizations = {
        item["name"]: item["num"] for item in queryset
    }
    queryset = (
        PersonVote.objects.filter(
            vote_event__legislative_session=legislative_session,
            voter__isnull=True,
        )
        .values(name=F("voter_name"))
        .annotate(num=Count("voter_name"))
    )
    report.unmatched_voters = {item["name"]: item["num"] for item in queryset}

    report.save()
    return report
