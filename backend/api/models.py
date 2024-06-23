from django.db import models

# Create your models here.
class Source(models.Model):
    
    class SourceType(models.TextChoices):
        SFTP = 'SFTP', 'SFTP'
        LOCALCOPY = 'LOCAL_COPY', 'Local Copy'
        HTTP = 'HTTP', 'HTTP'
        HTTPS = 'HTTPS', "HTTPS"
    
    name = models.CharField(max_length=20)
    hostname = models.CharField(max_length=100)
    ip_address = models.CharField(max_length=30)
    port = models.CharField(max_length=10, default='22')
    source_type = models.CharField(max_length=10, choices=SourceType.choices, default='LOCALCOPY')
    user_name = models.CharField(max_length=50)
    password = models.CharField(max_length=100)
    is_active = models.BooleanField(default=False)
    verified = models.BooleanField(default=False)
    system_message = models.CharField(max_length=255, null=True)
    created_on = models.DateTimeField(auto_now=True)
    updated_on = models.DateTimeField(auto_now_add=True)
    updated_by = models.CharField(max_length=50)

    def __str__(self):
        return f"sftp://{self.user_name}@{self.hostname}:{self.port}"

class DataPath(models.Model):
    
    class FileType(models.TextChoices):
        ALL = '*', 'All Files'
        TARGZ = 'TARGZ', '*.tar.gz'
        ZIP = 'ZIP', '*.zip'
        DAT1 = 'DAT1', '*.dat1'
        DAT2 = 'DAT2', '*.dat2'
    
    source = models.ForeignKey('Source', on_delete=models.CASCADE)
    directory_path = models.CharField(max_length=255)
    file_type = models.CharField(max_length=10, choices=FileType.choices, default='*')
    last_lookup_time = models.DateTimeField()
    auto_delete_enabled = models.BooleanField(default=False, help_text='Auto delete after file transfer completed.')
    is_active = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now=True)
    updated_on = models.DateTimeField(auto_now_add=True)
    updated_by = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.source}:{self.directory_path}"


class DataPipeline(models.Model):

    class PipelinePriority(models.TextChoices):
        HIGH = 'HIGH', 'High'
        NORMAL = 'NORMAL', 'Normal'
    name = models.CharField(max_length=255, help_text="Recommended format: 'source':'/path' ==> 'destination':'/path'")
    source = models.ForeignKey('DataPath', related_name='src_data_path', on_delete=models.CASCADE)
    destination = models.ForeignKey('DataPath', related_name='dst_data_path', on_delete=models.CASCADE)
    priority = models.CharField(max_length=10, choices=PipelinePriority.choices, default='NORMAL')
    cron_schedule = models.CharField(max_length=20, default="* * * * *")
    files_in_queue = models.IntegerField(default=0)
    last_run = models.DateTimeField(null=True, help_text='You may leave this blank. This will be filled when the pipeline starts')
    is_active = models.BooleanField(default=False)


class FileDetail(models.Model):
    filename = models.CharField(max_length=255)
    filesize_in_mb = models.BigIntegerField()
    managed_by_pipeline = models.ForeignKey('DataPipeline', on_delete=models.CASCADE)
    transfer_status = models.CharField(max_length=255)
    transfer_rate = models.CharField(max_length=255)
    archived = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now=True)
    updated_on = models.DateTimeField(auto_now_add=True)


    

