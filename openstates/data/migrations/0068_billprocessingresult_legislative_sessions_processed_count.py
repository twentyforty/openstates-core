# Generated by Django 4.1.1 on 2023-12-16 01:49

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("data", "0067_billprocessingresult_created_at"),
    ]

    operations = [
        migrations.AddField(
            model_name="billprocessingresult",
            name="legislative_sessions_processed_count",
            field=models.PositiveIntegerField(default=None, null=True),
        ),
    ]
