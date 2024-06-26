# Generated by Django 3.2.2 on 2021-09-20 19:34

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("data", "0038_auto_20210914_1559"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="eventsource",
            name="event",
        ),
        migrations.AddField(
            model_name="event",
            name="links",
            field=models.JSONField(blank=True, default=list),
        ),
        migrations.AddField(
            model_name="event",
            name="sources",
            field=models.JSONField(blank=True, default=list),
        ),
        migrations.DeleteModel(
            name="EventLink",
        ),
        migrations.DeleteModel(
            name="EventSource",
        ),
    ]
