# Generated by Django 4.1.1 on 2023-12-20 13:01

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("data", "0088_scrapednamematch_created_at"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="scrapednameunresolvedmatch",
            unique_together=None,
        ),
        migrations.RemoveField(
            model_name="scrapednameunresolvedmatch",
            name="chosen_option",
        ),
        migrations.RemoveField(
            model_name="scrapednameunresolvedmatch",
            name="legislative_session",
        ),
        migrations.AlterUniqueTogether(
            name="scrapednameunresolvedmatchoption",
            unique_together=None,
        ),
        migrations.RemoveField(
            model_name="scrapednameunresolvedmatchoption",
            name="membership",
        ),
        migrations.RemoveField(
            model_name="scrapednameunresolvedmatchoption",
            name="organization",
        ),
        migrations.RemoveField(
            model_name="scrapednameunresolvedmatchoption",
            name="unresolved_match",
        ),
        migrations.DeleteModel(
            name="ScrapedNameMatch",
        ),
        migrations.DeleteModel(
            name="ScrapedNameUnresolvedMatch",
        ),
        migrations.DeleteModel(
            name="ScrapedNameUnresolvedMatchOption",
        ),
    ]
