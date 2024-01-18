# Generated by Django 3.0.5 on 2020-04-23 11:00

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("data", "0004_auto_20200422_0040")]

    operations = [
        migrations.AddField(
            model_name="person",
            name="current_role_division_id",
            field=models.CharField(default="", max_length=100),
        ),
        migrations.AddField(
            model_name="person",
            name="primary_party",
            field=models.CharField(
                default="",
                help_text="Primary party an individual is associated with.",
                max_length=100,
            ),
        ),
    ]
