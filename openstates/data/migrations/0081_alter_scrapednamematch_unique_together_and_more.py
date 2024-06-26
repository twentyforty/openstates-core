# Generated by Django 4.1.1 on 2023-12-19 15:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("data", "0080_remove_scrapednamematch_legislative_session_and_more"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="scrapednamematch",
            unique_together=set(),
        ),
        migrations.AddField(
            model_name="scrapednamematch",
            name="legislative_session",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="scraped_names",
                to="data.legislativesession",
            ),
        ),
        migrations.AddField(
            model_name="scrapednamematch",
            name="matched_membership",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="scraped_names",
                to="data.membership",
            ),
        ),
        migrations.AddField(
            model_name="scrapednamematch",
            name="matched_organization",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="sponsorships_scraped_names",
                to="data.organization",
            ),
        ),
        migrations.AlterUniqueTogether(
            name="scrapednamematch",
            unique_together={
                ("matched_membership", "value"),
                ("matched_organization", "value"),
            },
        ),
        migrations.RemoveField(
            model_name="scrapednamematch",
            name="membership",
        ),
        migrations.RemoveField(
            model_name="scrapednamematch",
            name="organization",
        ),
    ]
