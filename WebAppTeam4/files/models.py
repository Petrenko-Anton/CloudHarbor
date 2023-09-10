import os
from uuid import uuid4

from django.db import models


def update_filename(instance, filename):
    upload_to = 'uploads'
    ext = filename.split('.')[-1]
    filename = f"{uuid4().hex}.{ext}"
    return os.path.join(upload_to, filename)


# Create your models here.
class File(models.Model):
    description = models.CharField(max_length=255)
    path = models.FileField(upload_to=update_filename)
    category = models.CharField(max_length=255, blank=True)
    # Списки суфіксів для сортування
    #
    # def get_file_category(file_name):
    #     ext = os.path.splitext(file_name)[1].lower()
    #     list_img = ['.jpg', '.jpeg', '.png', '.svg', '.bmp', '.svg', '.gif', '.webp',
    #                 '.tiff', '.ico', '.psd', '.eps', '.pict', '.pcx', '.cdr', '.ai', '.raw']
    #     list_archives = ['.zip', '.gz', '.tar', '.rar', '.7z', '.dmg', '.iso']
    #     list_videos = ['.avi', '.flv', '.wmv', '.mov', '.mp4', '.webm', '.vob', '.mpg',
    #                    '.mpeg', '.3gp', '.mkv', '.swf', '.ifo', '.rm', '.ra', '.ram', '.m2v', '.m2p']
    #     list_documents = ['.log', '.txt', '.doc', '.docx', '.docm', '.pdf', '.md', '.epub', '.ods', '.dotx',
    #                       '.odt', '.xml', '.ppt', '.pptx', '.csv', '.xls', '.xlsx', '.wpd', '.rtf', '.rtfd', '.rvg',
    #                       '.dox']
    #     list_musics = ['.aac', '.m4a', '.mp3', '.ogg', '.wav', '.wma', '.amr', '.midi', '.flac', '.alac', '.aiff',
    #                    '.mqa', '.dsd', '.asf', '.vqf', '.3ga']
    #     list_programs = ['.html', '.htm', '.xhtml', '.exe', '.msi', '.py', '.pyw', '.apk', '.npbk', '.torrent',
    #                      '.fig']
    #     if ext in list_img:
    #         return 'Зображення'
    #     elif ext in list_archives:
    #         return 'Архів'
    #     elif ext in list_videos:
    #         return 'Відео'
    #     elif ext in list_documents:
    #         return 'Документи'
    #     elif ext in list_musics:
    #         return 'Аудіо'
    #     elif ext in list_programs:
    #         return 'Програми'
    #     else:
    #         return 'Інше'

    def save(self, *args, **kwargs):
        if not self.category:  # Якщо категорія ще не визначена
            self.category = self.get_file_category(self.path.name)
        super().save(*args, **kwargs)