# Generated by Django 4.1.1 on 2023-12-20 13:01

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ("data", "0089_alter_scrapednameunresolvedmatch_unique_together_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="ScrapedNameUnresolvedMatch",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("value", models.CharField(db_index=True, max_length=300)),
                ("vote_ids", models.JSONField(default=list)),
                ("bill_sponsorship_ids", models.JSONField(default=list)),
            ],
            options={
                "db_table": "opencivicdata_scrapednameunresolvedmatch",
            },
        ),
        migrations.CreateModel(
            name="ScrapedNameUnresolvedMatchOption",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("score", models.FloatField(default=None, null=True)),
                (
                    "membership",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="scraped_name_unresolved_match_options",
                        to="data.membership",
                    ),
                ),
                (
                    "organization",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="scraped_name_unresolved_match_options",
                        to="data.organization",
                    ),
                ),
                (
                    "unresolved_match",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="options",
                        to="data.scrapednameunresolvedmatch",
                    ),
                ),
            ],
            options={
                "db_table": "opencivicdata_scrapednameunresolvedmatchoption",
            },
        ),
        migrations.AddField(
            model_name="scrapednameunresolvedmatch",
            name="chosen_option",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="chosen",
                to="data.scrapednameunresolvedmatchoption",
            ),
        ),
        migrations.AddField(
            model_name="scrapednameunresolvedmatch",
            name="legislative_session",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="scraped_name_unresolved_matches",
                to="data.legislativesession",
            ),
        ),
        migrations.CreateModel(
            name="ScrapedNameMatch",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("value", models.CharField(db_index=True, max_length=300)),
                ("approved", models.BooleanField(default=False)),
                ("vote_ids", models.JSONField(default=list)),
                ("bill_sponsorship_ids", models.JSONField(default=list)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "from_unresolved_match",
                    models.OneToOneField(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="matched_name",
                        to="data.scrapednameunresolvedmatch",
                    ),
                ),
                (
                    "legislative_session",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="scraped_names",
                        to="data.legislativesession",
                    ),
                ),
                (
                    "matched_membership",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="scraped_names",
                        to="data.membership",
                    ),
                ),
                (
                    "matched_organization",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="sponsorships_scraped_names",
                        to="data.organization",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "scraped name matches",
                "db_table": "opencivicdata_scrapednamematch",
            },
        ),
        migrations.AddConstraint(
            model_name="scrapednameunresolvedmatchoption",
            constraint=models.CheckConstraint(
                check=models.Q(
                    ("membership__isnull", False),
                    ("organization__isnull", False),
                    _connector="OR",
                ),
                name="unresolved_match_option_membership_xor_organization",
            ),
        ),
        migrations.AlterUniqueTogether(
            name="scrapednameunresolvedmatchoption",
            unique_together={
                ("unresolved_match", "membership"),
                ("unresolved_match", "organization"),
            },
        ),
        migrations.AlterUniqueTogether(
            name="scrapednameunresolvedmatch",
            unique_together={("legislative_session", "value")},
        ),
        migrations.AddConstraint(
            model_name="scrapednamematch",
            constraint=models.CheckConstraint(
                check=models.Q(
                    ("matched_membership__isnull", False),
                    ("matched_organization__isnull", False),
                    _connector="OR",
                ),
                name="scraped_name_match_membership_xor_organization",
            ),
        ),
        migrations.AlterUniqueTogether(
            name="scrapednamematch",
            unique_together={
                ("matched_organization", "value"),
                ("matched_membership", "value"),
            },
        ),
    ]
