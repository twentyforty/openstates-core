# Generated by Django 4.1.1 on 2024-01-11 01:58

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        (
            "data",
            "0108_remove_scrapednamematch_scraped_name_match_membership_xor_organization_and_more",
        ),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name="scrapednamematch",
            name="match_unique_organization_with_chamber",
        ),
        migrations.RemoveConstraint(
            model_name="scrapednamematch",
            name="match_unique_organization_without_chamber",
        ),
        migrations.RemoveConstraint(
            model_name="scrapednamematch",
            name="match_unique_person_with_chamber",
        ),
        migrations.RemoveConstraint(
            model_name="scrapednamematch",
            name="match_unique_person_without_chamber",
        ),
        migrations.RemoveConstraint(
            model_name="scrapednamematch",
            name="scraped_name_match_membership_xor_organization",
        ),
        migrations.RemoveConstraint(
            model_name="scrapednameunresolvedmatch",
            name="unique_with_chamber",
        ),
        migrations.RemoveConstraint(
            model_name="scrapednameunresolvedmatchoption",
            name="unresolved_match_option_membership_xor_organization",
        ),
        migrations.AddConstraint(
            model_name="scrapednamematch",
            constraint=models.UniqueConstraint(
                condition=models.Q(("matched_chamber__isnull", False)),
                fields=("legislative_session_id", "matched_chamber_id", "value"),
                name="match_unique_organization_with_chamber",
            ),
        ),
        migrations.AddConstraint(
            model_name="scrapednamematch",
            constraint=models.UniqueConstraint(
                condition=models.Q(("matched_chamber__isnull", True)),
                fields=("legislative_session_id", "value"),
                name="match_unique_without_chamber",
            ),
        ),
        migrations.AddConstraint(
            model_name="scrapednameunresolvedmatch",
            constraint=models.UniqueConstraint(
                condition=models.Q(("chamber__isnull", False)),
                fields=("legislative_session", "chamber", "value"),
                name="unique_with_chamber",
            ),
        ),
        migrations.AddConstraint(
            model_name="scrapednameunresolvedmatchoption",
            constraint=models.CheckConstraint(
                check=models.Q(
                    ("person__isnull", False),
                    ("organization__isnull", False),
                    _connector="OR",
                ),
                name="unresolved_match_option_membership_xor_organization",
            ),
        ),
    ]
