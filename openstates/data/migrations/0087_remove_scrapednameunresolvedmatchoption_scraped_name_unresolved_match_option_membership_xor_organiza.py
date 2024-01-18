# Generated by Django 4.1.1 on 2023-12-20 11:25

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("data", "0086_alter_scrapednameunresolvedmatchoption_unique_together"),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name="scrapednameunresolvedmatchoption",
            name="scraped_name_unresolved_match_option_membership_xor_organization",
        ),
        migrations.RenameField(
            model_name="scrapednameunresolvedmatchoption",
            old_name="scraped_name_unresolved_match",
            new_name="unresolved_match",
        ),
        migrations.AlterUniqueTogether(
            name="scrapednameunresolvedmatchoption",
            unique_together={
                ("unresolved_match", "organization"),
                ("unresolved_match", "membership"),
            },
        ),
        migrations.AddConstraint(
            model_name="scrapednameunresolvedmatchoption",
            constraint=models.CheckConstraint(
                check=models.Q(
                    ("membership__isnull", False),
                    ("organization__isnull", False),
                    _connector="OR",
                ),
                name="unresolved_match_option_membership_xor_organization",
            ),
        ),
    ]
