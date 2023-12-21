# Generated by Django 4.1.1 on 2023-12-21 12:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("data", "0091_alter_scrapednamematch_unique_together_and_more"),
    ]

    operations = [
        migrations.AddConstraint(
            model_name="personname",
            constraint=models.UniqueConstraint(
                fields=("name", "start_date", "end_date", "person_id"), name="unique_personname"
            ),
        ),
    ]