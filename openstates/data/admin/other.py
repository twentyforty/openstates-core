from collections.abc import Sequence
from logging import disable
from os import name
from django.contrib import admin
from django.db.models.query import QuerySet
from django.http.request import HttpRequest
from django.urls import reverse
from django.utils.html import format_html
from openstates.civiqa.publisher import publish_os_update_request
from openstates.data.admin.organization import OrganizationInline
from openstates.data.admin.reports import ScrapeReportInline, SessionDataQualityInline
from openstates.data.models.reports import BillProcessingResult
from admin_extra_buttons.api import (
    ExtraButtonsMixin,
    button,
    confirm_action,
    link,
    view,
)

from .. import models
from .base import ModelAdmin, ReadOnlyModelAdmin, ReadOnlyTabularInline


class JurisdictionInline(ReadOnlyTabularInline):
    model = models.Jurisdiction
    list_display = ("name", "id")
    readonly_fields = fields = (
        "get_id",
        "name",
        "classification",
        "extras",
        "url",
    )
    ordering = ("id",)

    def get_id(self, jurisdiction):
        admin_url = reverse("admin:data_jurisdiction_change", args=(jurisdiction.pk,))
        tmpl = '<a href="%s">%s</a>'
        return format_html(tmpl % (admin_url, jurisdiction.name))

    get_id.short_description = "ID"
    get_id.allow_tags = True
    get_id.admin_order_field = "jurisdiction__name"


@admin.register(models.Division)
class DivisionAdmin(ModelAdmin):
    list_display = ("name", "id")
    search_fields = list_display
    fields = ("id", "name", "redirect", "country")
    ordering = ("id",)
    inlines = [JurisdictionInline]
    autocomplete_fields = ("redirect",)


class LegislativeSessionInline(ReadOnlyTabularInline):
    model = models.LegislativeSession
    readonly_fields = (
        "identifier",
        "get_name",
        "active",
        "classification",
        "start_date",
        "end_date",
    )
    fields = readonly_fields
    ordering = ("-identifier",)

    def get_name(self, legislative_session):
        admin_url = reverse(
            "admin:data_legislativesession_change", args=(legislative_session.pk,)
        )
        tmpl = '<a href="%s">%s</a>'
        return format_html(tmpl % (admin_url, legislative_session.name))

    get_name.short_description = "NAME"
    get_name.allow_tags = True


class BillInline(ReadOnlyTabularInline):
    model = models.Bill
    max_num = 10
    readonly_fields = fields = (
        "get_identifier",
        "classification",
        "from_organization",
        "title",
        "latest_action_date",
        "subject",
    )
    ordering = ("identifier",)

    def get_identifier(self, bill):
        admin_url = reverse("admin:data_bill_change", args=(bill.id,))
        tmpl = '<a href="%s">%s</a>'
        return format_html(tmpl % (admin_url, bill.identifier))


@admin.register(BillProcessingResult)
class BillProcessingResultAdmin(ReadOnlyModelAdmin):
    readonly_fields = (
        "created_at",
        "run_plan",
        "legislative_session",
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
    fields = readonly_fields
    list_display = (
        "get_run_plan",
        "get_jurisdiction",
        "succeeded",
        "get_legislative_session",
        "processed_static_fields_bill_count",
        "processed_tags_bill_count",
        "processed_dynamic_fields_bill_count",
        "processed_progress_dates_bill_count",
        "processed_support_bill_count",
        "updated_gsheet_tracker_bill_count",
        "stats_calculated_legislative_session_count",
    )

    @admin.display(
        description="Jurisdiction", ordering="legislative_session__jurisdiction__name"
    )
    def get_jurisdiction(self, obj):
        if obj.legislative_session is None:
            return None
        admin_url = reverse(
            "admin:data_jurisdiction_change",
            args=(obj.legislative_session.jurisdiction_id,),
        )
        tmpl = '<a href="%s">%s</a>'
        return format_html(
            tmpl % (admin_url, obj.legislative_session.jurisdiction.name)
        )

    @admin.display(description="Run Plan", ordering="run_plan__id")
    def get_run_plan(self, obj):
        if obj.run_plan is None:
            return None
        admin_url = reverse("admin:data_runplan_change", args=(obj.run_plan_id,))
        tmpl = '<a href="%s">%s</a>'
        return format_html(tmpl % (admin_url, obj.run_plan.id))

    @admin.display(description="Session", ordering="legislative_session__identifier")
    def get_legislative_session(self, obj):
        if obj.legislative_session is None:
            return None
        admin_url = reverse(
            "admin:data_legislativesession_change", args=(obj.legislative_session_id,)
        )
        tmpl = '<a href="%s">%s</a>'
        return format_html(tmpl % (admin_url, obj.legislative_session.identifier))

    def get_list_select_related(self, request: HttpRequest) -> Sequence[str]:
        value = super().get_list_select_related(request) or []
        return value + [
            "legislative_session",
            "legislative_session__jurisdiction",
            "run_plan",
        ]


class BillProcessingResultAdminInline(ReadOnlyTabularInline):
    model = BillProcessingResult
    ordering = ("-created_at",)
    max_num = 1
    readonly_fields = (
        "get_created_at",
        "succeeded",
        "run_plan",
        "processed_static_fields_bill_count",
        "processed_tags_bill_count",
        "processed_dynamic_fields_bill_count",
        "processed_progress_dates_bill_count",
        "processed_support_bill_count",
        "updated_gsheet_tracker_bill_count",
        "stats_calculated_legislative_session_count",
    )
    fields = readonly_fields

    @admin.display(description="Created At", ordering="created_at")
    def get_created_at(self, obj):
        href = reverse("admin:data_billprocessingresult_change", args=(obj.pk,))
        display = obj.created_at.strftime("%Y-%m-%d %H:%M:%S")
        tmpl = '<a href="%s">%s</a>' % (href, display)
        return format_html(tmpl)


@admin.register(models.LegislativeSession)
class LegislativeSessionAdmin(ExtraButtonsMixin, ReadOnlyModelAdmin):
    search_fields = (
        "jurisdiction__name",
        "identifier",
        "name",
    )
    readonly_fields = (
        "jurisdiction",
        "identifier",
        "name",
        "active",
        "classification",
        "start_date",
        "end_date",
    )
    fields = readonly_fields
    inlines = [
        ScrapeReportInline,
        SessionDataQualityInline,
        BillProcessingResultAdminInline,
    ]
    list_display = (
        "identifier",
        "get_jurisdiction",
        "active",
        "name",
        "classification",
    )
    list_filter = (
        "active",
        "classification",
        ("jurisdiction", admin.RelatedOnlyFieldListFilter),
    )
    actions = ["trigger_scraper"]

    @admin.action(description="Trigger Scrape")
    def trigger_scraper(self, request, queryset: QuerySet):
        for legislative_session in queryset:
            publish_os_update_request(
                legislative_session=legislative_session, scrapers=["bills"]
            )
    
    @button(label="Trigger Scrape", disable_on_click=True)
    def trigger_scraper_button(self, request, pk):
        legislative_session = self.get_object(request, pk)
        publish_os_update_request(
            legislative_session=legislative_session, scrapers=["bills"]
        )

    @admin.display(description="Jurisdiction", ordering="jurisdiction__name")
    def get_jurisdiction(self, obj):
        admin_url = reverse(
            "admin:data_jurisdiction_change", args=(obj.jurisdiction.pk,)
        )
        tmpl = '<a href="%s">%s</a>'
        return format_html(tmpl % (admin_url, obj.jurisdiction.name))

    def get_list_select_related(self, request: HttpRequest) -> Sequence[str]:
        value = super().get_list_select_related(request) or []
        if "jurisdiction" not in value:
            value.append("jurisdiction")
        return value


@admin.register(models.Jurisdiction)
class JurisdictionAdmin(ModelAdmin):
    list_display = ("name", "id", "classification")
    readonly_fields = fields = (
        "id",
        "name",
        "division",
        "classification",
        "extras",
        "url",
    )
    fields = readonly_fields
    ordering = (
        "-classification",
        "id",
    )
    search_fields = ("id", "name")
    autocomplete_fields = ("division",)
    inlines = [LegislativeSessionInline, OrganizationInline]

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .prefetch_related("legislative_sessions", "organizations")
        )
