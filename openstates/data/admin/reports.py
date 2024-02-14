#  type: ignore
from django.contrib import admin
from openstates.data.admin.other import LegislativeSessionInline

from openstates.data.models.reports import BillProcessingResult  # type: ignore
from .. import models


class ScrapeReportInline(admin.TabularInline):
    model = models.ScrapeReport
    readonly_fields = ("scraper", "args", "start_time", "end_time", "get_object_list")

    def has_add_permission(self, request, obj=None):
        return False

    can_delete = False

    def get_object_list(self, obj):
        return "\n".join(
            "{} ({})".format(o.object_type, o.count) for o in obj.scraped_objects.all()
        )


class ImportObjectsInline(admin.TabularInline):
    model = models.ImportObjects
    readonly_fields = (
        "object_type",
        "insert_count",
        "update_count",
        "noop_count",
        "start_time",
        "end_time",
    )

    def has_add_permission(self, request, obj=None):
        return False

    can_delete = False


@admin.register(models.RunPlan)
class RunPlanAdmin(admin.ModelAdmin):
    actions = None

    readonly_fields = (
        "jurisdiction",
        "success",
        "start_time",
        "end_time",
        "exception",
        "traceback",
    )
    list_display = ("jurisdiction", "success", "start_time")
    inlines = [ScrapeReportInline, ImportObjectsInline]

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False


class RunPlanInline(admin.TabularInline):
    model = models.RunPlan
    readonly_fields = (
        "success",
        "start_time",
        "end_time",
        "exception",
        "traceback",
    )

    def has_add_permission(self, request, obj=None):
        return False

    can_delete = False


@admin.register(BillProcessingResult)
class BillProcessingResultAdmin(admin.ModelAdmin):
    actions = None

    readonly_fields = (
        "processed_static_fields_bill_count",
        "processed_tags_bill_count",
        "processed_dynamic_fields_bill_count",
        "processed_progress_dates_bill_count",
        "processed_support_bill_count",
        "updated_gsheet_tracker_bill_count",
        "stats_calculated_legislative_session_count",
        "succeeded",
        "exception",
    )
    
    inlines = [RunPlanInline, LegislativeSessionInline]


@admin.register(models.SessionDataQualityReport)
class SessionDataQualityAdmin(admin.ModelAdmin):
    actions = None

    readonly_fields = (
        "legislative_session",
        "bills_missing_actions",
        "bills_missing_sponsors",
        "bills_missing_versions",
        "votes_missing_voters",
        "votes_missing_bill",
        "votes_missing_yes_count",
        "votes_missing_no_count",
        "votes_with_bad_counts",
        "unmatched_sponsor_people",
        "unmatched_sponsor_organizations",
        "unmatched_voters",
    )
    list_display = (
        "jurisdiction_name",
        "legislative_session",
        "bills_missing_actions",
        "bills_missing_sponsors",
        "bills_missing_versions",
        "votes_missing_voters",
        "votes_missing_bill",
        "votes_missing_yes_count",
        "votes_missing_no_count",
        "votes_with_bad_counts",
    )

    def jurisdiction_name(self, obj):
        return obj.legislative_session.jurisdiction.name
