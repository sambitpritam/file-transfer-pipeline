# Generated by Django 4.2.13 on 2024-06-23 03:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0004_rename_updates_by_datapath_updated_by"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="FileRepo",
            new_name="FileDetail",
        ),
        migrations.AlterField(
            model_name="datapipeline",
            name="cron_schedule",
            field=models.CharField(default="* * * * *", max_length=20),
        ),
        migrations.AlterField(
            model_name="datapipeline",
            name="files_in_queue",
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name="datapipeline",
            name="last_run",
            field=models.DateTimeField(
                help_text="You may leave this blank. This will be filled when the pipeline starts",
                null=True,
            ),
        ),
    ]
