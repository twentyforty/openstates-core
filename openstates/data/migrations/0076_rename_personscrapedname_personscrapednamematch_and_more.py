# Generated by Django 4.1.1 on 2023-12-18 13:30

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("data", "0075_personscrapedname_vote_ids"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="PersonScrapedName",
            new_name="PersonScrapedNameMatch",
        ),
        migrations.AlterModelTable(
            name="personscrapednamematch",
            table="opencivicdata_personscrapednamematch",
        ),
    ]
