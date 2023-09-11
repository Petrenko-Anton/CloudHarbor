import os
import time

from django.conf import settings
from django_cron import CronJobBase, Schedule


class MyCronJob(CronJobBase):
    RUN_EVERY_MINS = 60  # Виконувати кожну годину

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'my_app.my_cron_job'  # Ім'я функції, яку потрібно викликати

    def cleanup_expired_media_files(self):
        media_root = settings.MEDIA_ROOT
        session_files_lifetime = 3600  # Тут ви можете встановити час життя файлів сесій у секундах

        current_time = time.time()
        for root, _, files in os.walk(media_root):
            for file_name in files:
                file_path = os.path.join(root, file_name)
                file_age = current_time - os.path.getmtime(file_path)

                if file_age > session_files_lifetime:
                    os.remove(file_path)
