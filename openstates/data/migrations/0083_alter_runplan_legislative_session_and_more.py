# Generated by Django 4.1.1 on 2023-12-19 19:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("data", "0082_alter_scrapednamematch_legislative_session"),
    ]

    operations = [
        migrations.AlterField(
            model_name="runplan",
            name="legislative_session",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="runs",
                to="data.legislativesession",
            ),
        ),
        migrations.AlterField(
            model_name="runplan",
            name="success",
            field=models.BooleanField(db_index=True, default=True),
        ),
    ]
