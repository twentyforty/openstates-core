# Generated by Django 3.0.5 on 2020-08-05 14:02

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [("data", "0013_remove_person_current_state")]

    operations = [
        migrations.RemoveField(model_name="person", name="current_role_division_id")
    ]
