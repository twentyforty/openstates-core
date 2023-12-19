from django.db import models
from django.db.models.fields import related
from openstates.data.models.base import RelatedBase
from openstates.data.models.people_orgs import Membership, Organization

from .jurisdiction import Jurisdiction, LegislativeSession

OBJECT_TYPES = (
    ("jurisdiction", "Jurisdiction"),
    ("person", "Person"),
    ("organization", "Organization"),
    ("post", "Post"),
    ("membership", "Membership"),
    ("bill", "Bill"),
    ("vote_event", "VoteEvent"),
    ("event", "Event"),
)


class RunPlan(models.Model):
    jurisdiction = models.ForeignKey(
        Jurisdiction, related_name="runs", on_delete=models.CASCADE
    )
    legislative_session = models.ForeignKey(
        LegislativeSession,
        on_delete=models.CASCADE,
        null=True,
        related_name="runs",
    )
    success = models.BooleanField(default=True, db_index=True)
    start_time = models.DateTimeField(db_index=True)
    end_time = models.DateTimeField(db_index=True)
    exception = models.TextField(blank=True, default="")
    traceback = models.TextField(blank=True, default="")

    class Meta:
        db_table = "pupa_runplan"


class ScrapeReport(models.Model):
    plan = models.ForeignKey(RunPlan, related_name="scrapers", on_delete=models.CASCADE)
    scraper = models.CharField(max_length=300)
    legislative_session = models.ForeignKey(
        LegislativeSession, on_delete=models.CASCADE, null=True
    )
    args = models.CharField(max_length=300)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    class Meta:
        db_table = "pupa_scrapereport"


class ScrapeObjects(models.Model):
    report = models.ForeignKey(
        ScrapeReport, related_name="scraped_objects", on_delete=models.CASCADE
    )
    object_type = models.CharField(max_length=20, choices=OBJECT_TYPES)
    count = models.PositiveIntegerField()

    class Meta:
        db_table = "pupa_scrapeobjects"


class ImportObjects(models.Model):
    plan = models.ForeignKey(
        RunPlan, related_name="imported_objects", on_delete=models.CASCADE
    )
    object_type = models.CharField(max_length=20, choices=OBJECT_TYPES)
    insert_count = models.PositiveIntegerField()
    update_count = models.PositiveIntegerField()
    noop_count = models.PositiveIntegerField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    records = models.JSONField(blank=True, null=True)

    class Meta:
        db_table = "pupa_importobjects"


class SessionDataQualityReport(models.Model):
    legislative_session = models.ForeignKey(
        LegislativeSession, on_delete=models.CASCADE
    )
    run_plan = models.OneToOneField(
        RunPlan,
        related_name="session_data_quality_report",
        on_delete=models.CASCADE,
        null=True,
    )
    bills_missing_actions = models.PositiveIntegerField()
    bills_missing_sponsors = models.PositiveIntegerField()
    bills_missing_versions = models.PositiveIntegerField()

    votes_missing_voters = models.PositiveIntegerField()
    votes_missing_bill = models.PositiveIntegerField()
    votes_missing_yes_count = models.PositiveIntegerField()
    votes_missing_no_count = models.PositiveIntegerField()
    votes_with_bad_counts = models.PositiveIntegerField()

    # these fields store lists of names mapped to numbers of occurances
    unmatched_sponsor_people = models.JSONField()
    unmatched_sponsor_organizations = models.JSONField()
    unmatched_voters = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "pupa_sessiondataqualityreport"


class BillProcessingResult(models.Model):
    run_plan = models.ForeignKey(
        RunPlan,
        related_name="bill_processing_results",
        on_delete=models.CASCADE,
        null=True,
    )
    legislative_session = models.ForeignKey(
        LegislativeSession, on_delete=models.CASCADE, null=True
    )
    processed_static_fields_bill_count = models.PositiveIntegerField(
        null=True, default=None
    )
    processed_tags_bill_count = models.PositiveIntegerField(null=True, default=None)
    processed_dynamic_fields_bill_count = models.PositiveIntegerField(
        null=True, default=None
    )
    processed_progress_dates_bill_count = models.PositiveIntegerField(
        null=True, default=None
    )
    processed_support_bill_count = models.PositiveIntegerField(null=True, default=None)
    updated_gsheet_tracker_bill_count = models.PositiveIntegerField(
        null=True, default=None
    )
    stats_calculated_legislative_session_count = models.PositiveIntegerField(
        null=True, default=None
    )
    legislative_sessions_processed_count = models.PositiveIntegerField(
        null=True, default=None
    )
    succeeded = models.BooleanField(default=True)
    exception = models.TextField(blank=True, default="", null=True)
    created_at = models.DateTimeField(auto_now_add=True)


class ScrapedNameMatch(RelatedBase):
    matched_membership = models.ForeignKey(
        Membership,
        related_name="scraped_names",
        on_delete=models.CASCADE,
        null=True,
    )
    matched_organization = models.ForeignKey(
        Organization,
        related_name="sponsorships_scraped_names",
        on_delete=models.CASCADE,
        null=True,
    )
    legislative_session = models.ForeignKey(
        LegislativeSession,
        on_delete=models.CASCADE,
        related_name="scraped_names",
    )
    value = models.CharField(max_length=300, db_index=True)
    approved = models.BooleanField(default=False)

    vote_ids = models.JSONField(default=list)
    bill_sponsorship_ids = models.JSONField(default=list)

    class Meta:
        db_table = "opencivicdata_scrapednamematch"
        unique_together = (
            ("matched_membership", "value"),
            ("matched_organization", "value"),
        )
        verbose_name_plural = "scraped name matches"

    def __str__(self):
        return f'"{self.value}"'
