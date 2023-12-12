from django.urls import reverse
from django.contrib import admin
from django.utils.safestring import mark_safe
from .. import models
from .base import (
    ModelAdmin,
    ReadOnlyTabularInline,
    IdentifierInline,
    OtherNameInline,
)


class PersonIdentifierInline(IdentifierInline):
    model = models.PersonIdentifier


class PersonNameInline(OtherNameInline):
    model = models.PersonName


class PersonOfficeInline(admin.TabularInline):
    fields = ("classification", "address", "voice", "fax", "name")
    model = models.PersonOffice


class PersonLinkInline(admin.TabularInline):
    fields = ("url", "note")
    model = models.PersonLink


class PersonSourceInline(admin.TabularInline):
    fields = ("url", "note")
    model = models.PersonSource


class MembershipInline(admin.TabularInline):
    model = models.Membership
    autocomplete_fields = ("organization", "person", "post")
    fields = (
        ("id",)
        + autocomplete_fields
        + (
            "role",
            "start_date",
            "end_date",
        )
    )
    exclude = ("id",)
    extra = 0
    can_delete = True
    ordering = ("end_date",)


# TODO field locking
@admin.register(models.Person)
class PersonAdmin(ModelAdmin):
    search_fields = ("id", "name", "current_jurisdiction__name")
    readonly_fields = (
        "id",
        "name",
        "extras",
        "image",
    )
    fields = (
        "id",
        "name",
        ("birth_date", "death_date"),
        "gender",
        "biography",
        "extras",
    )
    ordering = ("name",)
    inlines = [
        PersonIdentifierInline,
        PersonNameInline,
        PersonOfficeInline,
        PersonLinkInline,
        PersonSourceInline,
        MembershipInline,
    ]
    list_display = ("name", "id", "current_jurisdiction")

    # def get_memberships(self, obj):
    #     memberships = obj.memberships.select_related("organization__jurisdiction")
    #     html = []
    #     SHOW_N = 5
    #     for memb in memberships[:SHOW_N]:
    #         org = memb.organization
    #         admin_url = reverse("admin:data_organization_change", args=(org.pk,))
    #         tmpl = '<a href="%s">%s%s</a>\n'
    #         html.append(
    #             tmpl
    #             % (
    #                 admin_url,
    #                 (
    #                     memb.organization.jurisdiction.name + ": "
    #                     if memb.organization.jurisdiction
    #                     else ""
    #                 ),
    #                 memb.organization.name,
    #             )
    #         )
    #     more = len(memberships) - SHOW_N
    #     if 0 < more:
    #         html.append("And %d more" % more)
    #     return mark_safe("<br/>".join(html))

    # get_memberships.short_description = "Memberships"
