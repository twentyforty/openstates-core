# Generated by Django 4.1.1 on 2023-12-24 11:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("data", "0092_personname_unique_personname"),
    ]

    operations = [
        migrations.AddField(
            model_name="billsponsorship",
            name="person_organization",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="person_sponsorships",
                to="data.organization",
            ),
        ),
        migrations.AddField(
            model_name="billsponsorship",
            name="scraped_name_match_id",
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AddField(
            model_name="personname",
            name="scraped_name_match_id",
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AddField(
            model_name="personvote",
            name="scraped_name_match_id",
            field=models.PositiveIntegerField(null=True),
        ),
    ]