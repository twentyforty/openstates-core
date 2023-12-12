# Generated by Django 4.1.1 on 2022-10-23 04:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("data", "0057_alter_organization_classification"),
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
                    ("", "Unknown"),
                ],
                help_text="The type of Organization being defined.",
                max_length=100,
            ),
        ),
    ]
