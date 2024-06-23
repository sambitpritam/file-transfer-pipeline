from django.db import models

# Create your models here.
class ArchivalSetting(models.Model):
    auto_archival_days = models.IntegerField()
    auto_archival_paths = models.ForeignKey('api.DataPath', on_delete=models.CASCADE)
    default_percent_threshold = models.IntegerField(default=80)
    is_active = models.BooleanField(default=False)
    last_executed = models.DateTimeField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)