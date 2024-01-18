# Generated by Django 3.1.7 on 2021-04-01 14:49

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("data", "0030_auto_20210210_1817"),
    ]

    operations = [
        migrations.AddField(
            model_name="voteevent",
            name="dedupe_key",
            field=models.CharField(max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name="jurisdiction",
            name="classification",
            field=models.CharField(
                choices=[
                    ("state", "State"),
                    ("country", "Country"),
                    ("municipality", "Municipality"),
                ],
                db_index=True,
                default="state",
                help_text="The type of Jurisdiction being defined.",
                max_length=50,
            ),
        ),
    ]
