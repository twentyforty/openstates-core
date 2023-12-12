from django.contrib import admin
from django.template import defaultfilters
from .base import ReadOnlyModelAdmin, ReadOnlyTabularInline, IdentifierInline
from .. import models
from django.utils.html import format_html_join
from django.utils.html import format_html
from django.urls import reverse


class BillAbstractInline(ReadOnlyTabularInline):
    model = models.BillAbstract
    readonly_fields = ("abstract", "note")
    can_delete = False


class BillTitleInline(ReadOnlyTabularInline):
    model = models.BillTitle
    readonly_fields = ("title", "note")
    can_delete = False


class BillIdentifierInline(IdentifierInline):
    model = models.BillIdentifier
    fields = readonly_fields = ["identifier"]


class BillActionInline(ReadOnlyTabularInline):
    model = models.BillAction

    def get_related_entities(self, obj):
        ents = obj.related_entities.all()
        ent_list = [e.name for e in ents]
        return ", ".join(ent_list)

    get_related_entities.short_description = "Related Entities"
    get_related_entities.allow_tags = True

    list_select_related = ("BillActionRelatedEntity",)
    readonly_fields = fields = (
        "date",
        "organization",
        "description",
        "get_related_entities",
    )


class RelatedBillInline(ReadOnlyTabularInline):
    model = models.RelatedBill
    fk_name = "bill"
    readonly_fields = fields = ("identifier", "legislative_session", "relation_type")
    extra = 0


class BillSponsorshipInline(ReadOnlyTabularInline):
    model = models.BillSponsorship
    readonly_fields = fields = ("person", "primary", "classification")
    ordering = ("classification", "name")
    extra = 0


class DocVersionInline(ReadOnlyTabularInline):
    model = models.BillVersion

    def title_field(self, model: models.BillVersion):
        admin_url = reverse(
            "admin:%s_%s_change" % (model._meta.app_label, model._meta.model_name),
            args=[model.id],
        )
        tmpl = '<a href="%s">%s</a>'
        return format_html(tmpl % (admin_url, model.note[:10]))

    title_field.short_description = "Note"
    title_field.allow_tags = True

    list_select_related = ("BillVersionLink",)
    readonly_fields = (
        "title_field",
        "date",
    )


class BillVersionInline(DocVersionInline):
    model = models.BillVersion


class BillDocumentInline(DocVersionInline):
    model = models.BillDocument


class BillSourceInline(ReadOnlyTabularInline):
    readonly_fields = ("url", "note")
    model = models.BillSource


@admin.register(models.BillVersion)
class BillVersionAdmin(ReadOnlyModelAdmin):
    readonly_fields = fields = (
        "id",
        "note",
        "date",
        "classification",
        "extras",
    )


@admin.register(models.Bill)
class BillAdmin(ReadOnlyModelAdmin):
    readonly_fields = fields = (
        "identifier",
        "legislative_session",
        "bill_classifications",
        "from_organization",
        "title",
        "id",
        "subject",
        "extras",
    )
    search_fields = [
        "id",
        "identifier",
        "title",
        "legislative_session__jurisdiction__name",
    ]
    list_select_related = ("legislative_session", "legislative_session__jurisdiction")
    inlines = [
        BillAbstractInline,
        BillTitleInline,
        BillIdentifierInline,
        BillActionInline,
        BillSponsorshipInline,
        BillSourceInline,
        RelatedBillInline,
        BillVersionInline,
        BillDocumentInline,
    ]

    def bill_classifications(self, obj):
        return ", ".join(obj.classification)

    def get_jurisdiction_name(self, obj):
        return obj.legislative_session.jurisdiction.name

    get_jurisdiction_name.short_description = "Jurisdiction"

    def get_session_name(self, obj):
        return obj.legislative_session.name

    get_session_name.short_description = "Session"
    get_session_name.admin_order_field = "legislative_session__name"

    def get_truncated_sponsors(self, obj):
        spons = ", ".join(s.name for s in obj.sponsorships.all()[:5])
        return defaultfilters.truncatewords(spons, 10)

    get_truncated_sponsors.short_description = "Sponsors"

    def get_truncated_title(self, obj):
        return defaultfilters.truncatewords(obj.title, 25)

    get_truncated_title.short_description = "Title"

    list_display = (
        "identifier",
        "get_jurisdiction_name",
        "get_session_name",
        "get_truncated_sponsors",
        "get_truncated_title",
    )

    ordering = (
        "legislative_session__jurisdiction__name",
        "legislative_session",
        "identifier",
    )
