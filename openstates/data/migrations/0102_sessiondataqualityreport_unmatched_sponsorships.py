# Generated by Django 4.1.1 on 2024-01-02 16:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("data", "0101_alter_runplan_end_time_alter_runplan_start_time_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="sessiondataqualityreport",
            name="unmatched_sponsorships",
            field=models.JSONField(default={}),
            preserve_default=False,
        ),
    ]
