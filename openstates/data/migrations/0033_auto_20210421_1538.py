# Generated by Django 3.2 on 2021-04-21 15:38

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("data", "0032_event_dedupe_key"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="organizationsource",
            name="organization",
        ),
        migrations.AddField(
            model_name="organization",
            name="links",
            field=django.contrib.postgres.fields.jsonb.JSONField(
                default=list, blank=True
            ),
        ),
        migrations.AddField(
            model_name="organization",
            name="sources",
            field=django.contrib.postgres.fields.jsonb.JSONField(
                default=list, blank=True
            ),
        ),
        migrations.DeleteModel(
            name="OrganizationLink",
        ),
        migrations.DeleteModel(
            name="OrganizationSource",
        ),
    ]
