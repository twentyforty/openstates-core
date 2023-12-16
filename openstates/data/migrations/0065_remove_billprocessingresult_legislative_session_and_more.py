# Generated by Django 4.1.1 on 2023-12-13 16:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("data", "0064_billprocessingresult"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="billprocessingresult",
            name="legislative_session",
        ),
        migrations.AddField(
            model_name="billprocessingresult",
            name="exception",
            field=models.TextField(blank=True, default="", null=True),
        ),
        migrations.AddField(
            model_name="billprocessingresult",
            name="processed_dynamic_fields_bill_count",
            field=models.PositiveIntegerField(default=None, null=True),
        ),
        migrations.AddField(
            model_name="billprocessingresult",
            name="processed_progress_dates_bill_count",
            field=models.PositiveIntegerField(default=None, null=True),
        ),
        migrations.AddField(
            model_name="billprocessingresult",
            name="processed_static_fields_bill_count",
            field=models.PositiveIntegerField(default=None, null=True),
        ),
        migrations.AddField(
            model_name="billprocessingresult",
            name="processed_support_bill_count",
            field=models.PositiveIntegerField(default=None, null=True),
        ),
        migrations.AddField(
            model_name="billprocessingresult",
            name="processed_tags_bill_count",
            field=models.PositiveIntegerField(default=None, null=True),
        ),
        migrations.AddField(
            model_name="billprocessingresult",
            name="processed_vote_event_count",
            field=models.PositiveIntegerField(default=None, null=True),
        ),
        migrations.AddField(
            model_name="billprocessingresult",
            name="succeeded",
            field=models.BooleanField(default=True),
        ),
    ]