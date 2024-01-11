# Generated by Django 4.1.1 on 2024-01-11 01:24

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("data", "0104_scrapednamematch_scrapednameunresolvedmatch_and_more"),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name="scrapednamematch",
            name="match_unique_with_chamber",
        ),
        migrations.RemoveConstraint(
            model_name="scrapednamematch",
            name="match_unique_without_chamber",
        ),
        migrations.AddConstraint(
            model_name="scrapednamematch",
            constraint=models.UniqueConstraint(
                condition=models.Q(("matched_chamber__isnull", False)),
                fields=("legislative_session_id", "matched_chamber_id", "value"),
                name="match_unique_with_chamber",
            ),
        ),
        migrations.AddConstraint(
            model_name="scrapednamematch",
            constraint=models.UniqueConstraint(
                condition=models.Q(("matched_chamber", None)),
                fields=("legislative_session_id", "value"),
                name="match_unique_without_chamber",
            ),
        ),
    ]
