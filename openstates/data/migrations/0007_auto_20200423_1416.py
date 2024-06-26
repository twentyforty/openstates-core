# Generated by Django 3.0.5 on 2020-04-23 14:16

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("data", "0006_auto_20200423_1124")]

    operations = [
        migrations.AlterField(
            model_name="bill",
            name="first_action_date",
            field=models.CharField(default="", max_length=25, null=True),
        ),
        migrations.AlterField(
            model_name="bill",
            name="latest_action_date",
            field=models.CharField(default="", max_length=25, null=True),
        ),
        migrations.AlterField(
            model_name="bill",
            name="latest_action_description",
            field=models.TextField(default="", null=True),
        ),
        migrations.AlterField(
            model_name="bill",
            name="latest_passage_date",
            field=models.CharField(default="", max_length=25, null=True),
        ),
    ]
