# Generated by Django 3.0.5 on 2020-07-21 16:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [("data", "0009_auto_20200429_0913")]

    operations = [
        migrations.AlterField(
            model_name="jurisdiction",
            name="division",
            field=models.ForeignKey(
                help_text="A link to a Division related to this Jurisdiction.",
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="jurisdictions",
                to="data.Division",
            ),
        )
    ]
