import paramiko.sftp_file
from api.models import *
from api import custom_logger

import paramiko
import os
import datetime

class ConfigValidator:

    def __init__(self) -> None:
        self.log = custom_logger.get_logger(__name__)
        self.start = None

    def verify_source_connectivity(self):
        sftp = None
        client = None
        try:
            sources = Source.objects.filter(
                verified__exact=False).filter(is_active__exact=True)
            for entry in sources:
                client, sftp = self.get_sftp_client(entry.id)

                if sftp is not None and client is not None:
                    entry.verified = True
                    entry.save()

        except Exception as e:
            self.log.error(f"{e}")

        finally:
            if sftp is not None:
                sftp.close()

            if client is not None:
                client.close()

    def get_sftp_client(self, id):
        # configuring paramiko size
        paramiko.sftp_file.SFTPFile.MAX_REQUEST_SIZE = pow(2, 22)
        sftp_object = Source.objects.filter(id__exact=id)
        if len(sftp_object) > 1:
            raise Exception("Unhandled Exception at get_sftp_client")
        for sftp_cred in sftp_object:
            client = paramiko.SSHClient()
            client.load_system_host_keys()
            client.connect(hostname=sftp_cred.ip_address,
                           port=int(sftp_cred.port),
                           username=sftp_cred.user_name,
                           password=sftp_cred.password
                           )
            sftp = paramiko.SFTPClient.from_transport(client.get_transport())

        return client, sftp

    def download_files(self, pipeline_name):
        sftp = None
        client = None
        transfer_result = []
        try:
            pipeline = DataPipeline.objects.filter(
                name__exact=pipeline_name).filter(is_active__exact=True).get()
            client, sftp = self.get_sftp_client(pipeline.source.id)

            if client is not None and sftp is not None:

                # files = sftp.listdir(path=pipeline.source.directory_path)
                files_attrs = sftp.listdir_attr(path=pipeline.source.directory_path)
                self.start = datetime.datetime.now()


                for f in files_attrs:
                    if (not os.path.exists(f"/workspaces/file-transfer-pipeline/tmp/downloads/task-{pipeline.source.id}")):
                        os.makedirs(f"/workspaces/file-transfer-pipeline/tmp/downloads/task-{pipeline.source.id}")
                    
                    local_dest = f"/workspaces/file-transfer-pipeline/tmp/downloads/task-{pipeline.source.id}/{f.filename}"
                    if pipeline.source.file_type == '*':
                        if os.path.exists(local_dest) and os.path.getsize(local_dest) == f.st_size:
                            continue
                        elif os.path.exists(local_dest) and os.path.getsize(local_dest) != f.st_size:
                            os.remove(local_dest)
                        
                        with open(local_dest, 'wb') as fwriter:
                            transfer_result.append(
                                sftp.getfo(
                                    f"{pipeline.source.directory_path}/{f.filename}", fwriter, self.transfer_status)
                            )
                    elif pipeline.source.file_type.replace('*', '') in f:
                        with open(local_dest, 'wb') as fwriter:
                            transfer_result.append(
                                sftp.getfo(
                                    f"{pipeline.source.directory_path}/{f.filename}", fwriter, self.transfer_status)
                            )

            pipeline.files_in_queue = len(transfer_result)
            pipeline.save()
        except Exception as e:
            self.log.error(f"{e}")

        finally:
            if sftp is not None:
                sftp.close()

            if client is not None:
                client.close()

    def transfer_status(self, sent, size):
        sent_mb = round(float(sent) / 1000000, 1)
        remaining_mb = round(float(size - sent) / 1000000, 1)
        size_mb = round(size / 1000000, 1)
        time = datetime.datetime.now()
        elapsed = time - self.start
        if sent > 0:
            remaining_seconds = elapsed.total_seconds() * (float(size - sent) / sent)
        else:
            remaining_seconds = 0
        remaining_hours, remaining_remainder = divmod(remaining_seconds, 3600)
        remaining_minutes, remaining_seconds = divmod(remaining_remainder, 60)
        self.log.info(
            ("Total size:{0} MB|Sent:{1} MB|Remaining:{2} MB|" +
            "Time remaining:{3:02}:{4:02}:{5:02}").
            format(
                size_mb, sent_mb, remaining_mb,
                int(remaining_hours), int(remaining_minutes), int(remaining_seconds)))
