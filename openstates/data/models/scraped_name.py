from django.db import models, transaction
from django.db.models import Q, CheckConstraint, UniqueConstraint
from django.utils import timezone
from openstates.data.models.jurisdiction import LegislativeSession
from openstates.data.models.people_orgs import Organization, Person


class ScrapedNameMatch(models.Model):
    matched_person = models.ForeignKey(
        Person,
        related_name="scraped_names",
        on_delete=models.CASCADE,
        null=True,
    )
    matched_chamber = models.ForeignKey(
        Organization,
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

    from_unresolved_match = models.OneToOneField(
        "ScrapedNameUnresolvedMatch",
        on_delete=models.SET_NULL,
        null=True,
        related_name="matched_name",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField()
    class Meta:
        constraints = [
            UniqueConstraint(
                fields=["legislative_session_id", "matched_chamber_id", "value"],
                condition=Q(matched_chamber__isnull=False),
                name="match_unique_organization_with_chamber",
            ),
            UniqueConstraint(
                fields=["legislative_session_id", "value"],
                condition=Q(matched_chamber__isnull=True),
                name="match_unique_without_chamber",
            ),
            
            # CheckConstraint(
            #     check=Q(matched_person__isnull=False, matched_organization__isnull=True)
            #     | Q(matched_person__isnull=True, matched_organization__isnull=False),
            #     name="scraped_name_match_membership_xor_organization",
            # ),
        ]
        verbose_name_plural = "scraped name matches"

    def __str__(self):
        return f'"{self.value}"'


# enum of textchoices
class ScrapedNameMatchResolution(models.TextChoices):
    PENDING = "pending", "Pending"
    MATCHED = "matched", "Matched"
    AMBIGUOUS = "ambiguous", "Ambiguous"
    NO_MATCH = "no_match", "No Match"
    IGNORE = "ignore", "Ignore"
    NEEDS_PERSON = "needs_person", "Needs Person"
    NEEDS_COMMITTEE = "needs_committee", "Needs Committee"
    NEEDS_ATTENTION = "needs_attention", "Needs Attention"


class ScrapedNameUnresolvedMatch(models.Model):
    legislative_session = models.ForeignKey(
        LegislativeSession,
        on_delete=models.CASCADE,
        related_name="scraped_name_unresolved_matches",
    )
    value = models.CharField(max_length=300, db_index=True)
    chamber = models.ForeignKey(
        Organization,
        related_name="scraped_names_unresolved_matches",
        on_delete=models.CASCADE,
        null=True,
    )
    chosen_option = models.ForeignKey(
        "ScrapedNameUnresolvedMatchOption",
        related_name="chosen",
        on_delete=models.SET_NULL,
        null=True,
    )
    resolution = models.CharField(
        max_length=50,
        choices=ScrapedNameMatchResolution.choices,
        blank=True,
        default=ScrapedNameMatchResolution.PENDING,
    )
    resolution_note = models.TextField(blank=True, default="")
    vote_ids = models.JSONField(default=list)
    bill_sponsorship_ids = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField()

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=["legislative_session", "chamber", "value"],
                condition=Q(chamber__isnull=False),
                name="unique_with_chamber",
            ),
            UniqueConstraint(
                fields=["legislative_session", "value"],
                condition=Q(chamber=None),
                name="unique_without_chamber",
            ),
        ]

    @property
    def resolved(self):
        return self.chosen_option is not None

    def resolve(self, option: "ScrapedNameUnresolvedMatchOption"):
        if self.chosen_option == option:
            return
        with transaction.atomic():
            self.chosen_option = option
            self.resolution = ScrapedNameMatchResolution.MATCHED
            self.save()

            updated_at = timezone.now()
            
            return ScrapedNameMatch.objects.update_or_create(
                matched_person=option.person,
                matched_chamber=self.chamber,
                matched_organization=option.organization,
                value=self.value,
                legislative_session=self.legislative_session,
                defaults=dict(
                    from_unresolved_match=self,
                    vote_ids=self.vote_ids,
                    bill_sponsorship_ids=self.bill_sponsorship_ids,
                    updated_at=updated_at,
                ),
            )[0]

    def __str__(self):
        if self.chosen_option:
            return f'unresolved match ({self.resolution}): "{self.value}" = "{self.chosen_option.person or self.chosen_option.organization}"'
        return f'unresolved match ({self.resolution}): "{self.value}"?'


class ScrapedNameUnresolvedMatchOption(models.Model):
    unresolved_match = models.ForeignKey(
        ScrapedNameUnresolvedMatch,
        related_name="options",
        on_delete=models.CASCADE,
    )
    person = models.ForeignKey(
        Person,
        related_name="scraped_name_unresolved_match_options",
        on_delete=models.CASCADE,
        null=True,
    )
    chamber = models.ForeignKey(
        Organization,
        related_name="scraped_name_unresolved_person_match_options",
        on_delete=models.CASCADE,
        null=True,
    )
    district = models.CharField(max_length=300, null=True, default=None)
    organization = models.ForeignKey(
        Organization,
        related_name="scraped_name_unresolved_sponsorship_match_options",
        on_delete=models.CASCADE,
        null=True,
    )
    score = models.FloatField(null=True, default=None)

    def choose(self):
        return self.unresolved_match.resolve(self)

    class Meta:
        unique_together = (
            ("unresolved_match", "person", "chamber"),
            ("unresolved_match", "organization"),
        )
        constraints = [
            models.CheckConstraint(
                check=models.Q(person__isnull=False) | models.Q(organization__isnull=False),
                name="unresolved_match_option_membership_xor_organization",
            )
        ]

    def __str__(self):
        return f'unresolved match option: "{self.person or self.organization}" ?? "{self.unresolved_match.value}"'
