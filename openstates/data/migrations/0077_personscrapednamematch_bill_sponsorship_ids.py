# Generated by Django 4.1.1 on 2023-12-19 08:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("data", "0076_rename_personscrapedname_personscrapednamematch_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="personscrapednamematch",
            name="bill_sponsorship_ids",
            field=models.JSONField(default=list),
        ),
    ]
