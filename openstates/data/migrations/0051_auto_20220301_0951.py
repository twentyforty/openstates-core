# Generated by Django 3.2.8 on 2022-03-01 09:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("data", "0050_alter_organization_classification"),
    ]

    operations = [
        migrations.AlterField(
            model_name="billdocument",
            name="classification",
            field=models.CharField(
                blank=True,
                choices=[
                    ("", "Unknown"),
                    ("fiscal-note", "Fiscal Note"),
                    ("committee-report", "Committee Report"),
                    ("summary", "Summary"),
                    ("digest", "Digest"),
                    ("veto-message", "Veto Message"),
                    ("analysis", "Analysis"),
                    ("law", "Law"),
                    ("", "Unknown"),
                ],
                max_length=100,
            ),
        ),
        migrations.AlterField(
            model_name="eventdocument",
            name="classification",
            field=models.CharField(
                blank=True,
                choices=[
                    ("agenda", "Agenda"),
                    ("minutes", "Minutes"),
                    ("transcript", "Transcript"),
                    ("testimony", "Testimony"),
                    ("", "Unknown"),
                ],
                max_length=50,
            ),
        ),
        migrations.AlterField(
            model_name="eventmedia",
            name="classification",
            field=models.CharField(
                blank=True,
                choices=[
                    ("audio recording", "Audio Recording"),
                    ("video recording", "Video Recording"),
                    ("", "Unknown"),
                ],
                max_length=50,
            ),
        ),
        migrations.AlterField(
            model_name="legislativesession",
            name="classification",
            field=models.CharField(
                blank=True,
                choices=[
                    ("primary", "Primary"),
                    ("special", "Special"),
                    ("", "Unknown"),
                ],
                max_length=100,
            ),
        ),
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
                    ("", "Unknown"),
                ],
                help_text="The type of Organization being defined.",
                max_length=100,
            ),
        ),
        migrations.AlterField(
            model_name="personvote",
            name="option",
            field=models.CharField(
                choices=[
                    ("yes", "Yes"),
                    ("no", "No"),
                    ("absent", "Absent"),
                    ("abstain", "Abstain"),
                    ("not voting", "Not Voting"),
                    ("paired", "Paired"),
                    ("excused", "Excused"),
                    ("other", "Other"),
                    ("", "Unknown"),
                ],
                max_length=50,
            ),
        ),
        migrations.AlterField(
            model_name="votecount",
            name="option",
            field=models.CharField(
                choices=[
                    ("yes", "Yes"),
                    ("no", "No"),
                    ("absent", "Absent"),
                    ("abstain", "Abstain"),
                    ("not voting", "Not Voting"),
                    ("paired", "Paired"),
                    ("excused", "Excused"),
                    ("other", "Other"),
                    ("", "Unknown"),
                ],
                max_length=50,
            ),
        ),
    ]