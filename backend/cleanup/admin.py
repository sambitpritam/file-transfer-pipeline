from django.contrib import admin
from .models import *


# Register your models here.
class ArchivalSettingAdmin(admin.ModelAdmin):
    list_display = [
        'auto_archival_paths',
        'auto_archival_days',
        'default_percent_threshold',
        'is_active',
        'last_executed',
        'updated_on',
    ]

admin.site.register(ArchivalSetting, ArchivalSettingAdmin)