# Generated by Django 4.2.13 on 2024-06-23 03:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0003_source_port"),
    ]

    operations = [
        migrations.RenameField(
            model_name="datapath",
            old_name="updates_by",
            new_name="updated_by",
        ),
    ]
