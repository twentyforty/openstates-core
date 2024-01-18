# Generated by Django 3.0.5 on 2020-04-29 09:13

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("data", "0008_person_current_state")]

    operations = [
        migrations.AlterField(
            model_name="bill",
            name="first_action_date",
            field=models.CharField(default=None, max_length=25, null=True),
        ),
        migrations.AlterField(
            model_name="bill",
            name="latest_action_date",
            field=models.CharField(default=None, max_length=25, null=True),
        ),
        migrations.AlterField(
            model_name="bill",
            name="latest_action_description",
            field=models.TextField(default=""),
        ),
        migrations.AlterField(
            model_name="bill",
            name="latest_passage_date",
            field=models.CharField(default=None, max_length=25, null=True),
        ),
    ]
