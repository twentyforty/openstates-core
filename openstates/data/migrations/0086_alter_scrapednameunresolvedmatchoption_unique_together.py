# Generated by Django 4.1.1 on 2023-12-20 10:58

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("data", "0085_scrapednameunresolvedmatch_and_more"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="scrapednameunresolvedmatchoption",
            unique_together={
                ("scraped_name_unresolved_match", "membership"),
                ("scraped_name_unresolved_match", "organization"),
            },
        ),
    ]
