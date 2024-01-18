# Generated by Django 4.1.1 on 2023-12-13 23:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("data", "0065_remove_billprocessingresult_legislative_session_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="billprocessingresult",
            old_name="plan",
            new_name="run_plan",
        ),
        migrations.RenameField(
            model_name="billprocessingresult",
            old_name="processed_vote_event_count",
            new_name="stats_calculated_legislative_session_count",
        ),
        migrations.AddField(
            model_name="billprocessingresult",
            name="legislative_session",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="data.legislativesession",
            ),
        ),
        migrations.AddField(
            model_name="billprocessingresult",
            name="updated_gsheet_tracker_bill_count",
            field=models.PositiveIntegerField(default=None, null=True),
        ),
    ]
