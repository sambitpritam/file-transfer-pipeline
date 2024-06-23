from django.contrib import admin
from .models import *

# Register your models here.
# models: Source, DataPath, DataPipeline, FileRepo

class SourceAdmin(admin.ModelAdmin):
    list_display =(
        'id',
        'name',
        'hostname',
        'source_type',
        'is_active',
        'verified',
        'updated_on',
        'updated_by',
    )

class DataPathAdmin(admin.ModelAdmin):
    list_display = (
        'source',
        'directory_path',
        'file_type',
        'last_lookup_time',
        'auto_delete_enabled',
        'is_active',
        'updated_on',
        'updated_by',
    )

class DataPipelineAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'source',
        'destination',
        'priority',
        'cron_schedule',
        'files_in_queue',
        'last_run',
        'is_active',
    )

class FileDetailAdmin(admin.ModelAdmin):
    list_display = (
        'filename',
        'filesize_in_mb',
        'managed_by_pipeline',
        'transfer_status',
        'transfer_rate',
        'archived',
        'updated_on',
    )


admin.site.register(Source, SourceAdmin)
admin.site.register(DataPath, DataPathAdmin)
admin.site.register(DataPipeline, DataPipelineAdmin)
admin.site.register(FileDetail, FileDetailAdmin)
