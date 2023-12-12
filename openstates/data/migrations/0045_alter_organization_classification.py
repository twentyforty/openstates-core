# Generated by Django 3.2.8 on 2021-11-19 11:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("data", "0044_bill_citations"),
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
                ],
                help_text="The type of Organization being defined.",
                max_length=100,
            ),
        ),
    ]
