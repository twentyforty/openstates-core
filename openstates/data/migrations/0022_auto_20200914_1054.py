# Generated by Django 3.0.5 on 2020-09-14 10:54

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("data", "0021_remove_jurisdiction_feature_flags"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="organization",
            name="dissolution_date",
        ),
        migrations.RemoveField(
            model_name="organization",
            name="founding_date",
        ),
        migrations.RemoveField(
            model_name="organization",
            name="image",
        ),
    ]
