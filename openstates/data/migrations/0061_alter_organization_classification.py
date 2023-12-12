# Generated by Django 4.1.1 on 2022-11-15 15:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("data", "0060_alter_membership_post_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="organization",
            name="classification",
            field=models.CharField(
                blank=True,
                choices=[
                    ("legislature", "Legislature"),
                    ("executive", "Executive"),
                    ("upper", "Upper Chamber"),
                    ("lower", "Lower Chamber"),
                    ("party", "Party"),
                    ("committee", "Committee"),
                    ("government", "Government"),
                    ("subcommittee", "Subcommittee"),
                    ("judicial", "Judicial"),
                    ("school", "School"),
                    ("governing_board", "Governing board"),
                    ("administrative", "Administrative"),
                    ("advisory", "Advisory"),
                    ("managerial", "Managerial"),
                    ("police", "Police"),
                    ("shool_board", "School board"),
                    ("fire", "Fire"),
                    ("", "Unknown"),
                ],
                help_text="The type of Organization being defined.",
                max_length=100,
            ),
        ),
    ]
