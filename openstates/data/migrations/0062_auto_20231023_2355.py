# Generated by Django 3.2.14 on 2023-10-23 23:55

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("data", "0061_alter_organization_classification"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="billaction",
            options={"ordering": ["date", "order"]},
        ),
        migrations.AlterField(
            model_name="billdocument",
            name="note",
            field=models.CharField(max_length=3000),
        ),
        migrations.AlterField(
            model_name="billversion",
            name="note",
            field=models.CharField(max_length=3000),
        ),
    ]
