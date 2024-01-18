# Generated by Django 3.2.8 on 2022-08-28 05:37

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("data", "0054_alter_jurisdiction_classification"),
    ]

    operations = [
        migrations.AlterField(
            model_name="jurisdiction",
            name="classification",
            field=models.CharField(
                choices=[
                    ("state", "State"),
                    ("country", "Country"),
                    ("municipality", "Municipality"),
                    ("school_district", "School district"),
                ],
                db_index=True,
                default="state",
                help_text="The type of Jurisdiction being defined.",
                max_length=50,
            ),
        ),
    ]
