#  type: ignore
from collections.abc import Sequence
from typing import Any

from django.contrib import admin
from django.db.models.query import QuerySet
from django.http.request import HttpRequest
from django.urls import reverse
from django.utils.html import format_html
from openstates.data.admin.base import ReadOnlyModelAdmin, ReadOnlyTabularInline

from .. import models


class ScrapeReportInline(admin.TabularInline):
    model = models.ScrapeReport
    readonly_fields = (
        "legislative_session",
        "scraper",
        "args",
        "start_time",
        "end_time",
        "get_object_list",
    )
    fields = readonly_fields

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
    fields = readonly_fields

    def has_add_permission(self, request, obj=None):
        return False

    can_delete = False


@admin.register(models.RunPlan)
class RunPlanAdmin(ReadOnlyModelAdmin):
    actions = None

    readonly_fields = (
        "jurisdiction",
        "success",
        "start_time",
        "end_time",
        "exception",
        "traceback",
    )
    list_display = ("id", "jurisdiction", "success", "start_time")
    inlines = [ScrapeReportInline, ImportObjectsInline]
    list_filter = (("jurisdiction", admin.RelatedOnlyFieldListFilter), "success")
    search_fields = ("jurisdiction__name", "id")
    
    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False


class RunPlanInline(ReadOnlyTabularInline):
    model = models.RunPlan
    readonly_fields = (
        "success",
        "start_time",
        "end_time",
        "exception",
        "traceback",
    )
    fields = readonly_fields


@admin.register(models.SessionDataQualityReport)
class SessionDataQualityAdmin(ReadOnlyModelAdmin):
    actions = None
    search_fields = (
        "legislative_session__identifier",
        "legislative_session__jurisdiction__name",
        "id",
    )
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
    fields = readonly_fields
    list_display = (
        "id",
        "get_jurisdiction",
        "legislative_session__identifier",
        "bills_missing_actions",
        "bills_missing_sponsors",
        "bills_missing_versions",
        "votes_missing_voters",
        "votes_missing_bill",
        "votes_missing_yes_count",
        "votes_missing_no_count",
        "votes_with_bad_counts",
    )

    @admin.display(description="Session", ordering="legislative_session__identifier")
    def legislative_session__identifier(self, obj):
        return obj.legislative_session.identifier

    @admin.display(
        description="Jurisdiction", ordering="legislative_session__jurisdiction__name"
    )
    def get_jurisdiction(self, obj):
        jurisdiction = obj.legislative_session.jurisdiction
        admin_url = reverse("admin:data_jurisdiction_change", args=(jurisdiction.pk,))
        tmpl = f'<a href="{admin_url}">{jurisdiction.name}</a>'
        return format_html(tmpl)

    def get_list_select_related(self, request: HttpRequest) -> Sequence[str]:
        value = super().get_list_select_related(request) or []
        value.append("legislative_session")
        value.append("legislative_session__jurisdiction")
        return value


class SessionDataQualityInline(ReadOnlyTabularInline):
    model = models.SessionDataQualityReport
    readonly_fields = (
        "id",
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
