# Generated by Django 4.1.1 on 2022-10-11 19:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("data", "0055_alter_jurisdiction_classification"),
    ]

    operations = [
        migrations.AlterField(
            model_name="eventlocation",
            name="name",
            field=models.CharField(max_length=2000),
        ),
    ]
