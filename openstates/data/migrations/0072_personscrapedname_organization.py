# Generated by Django 4.1.1 on 2023-12-17 13:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("data", "0071_personscrapedname"),
    ]

    operations = [
        migrations.AddField(
            model_name="personscrapedname",
            name="organization",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="scraped_names",
                to="data.organization",
            ),
        ),
    ]
