import os
from uuid import uuid4
from .utils import get_file_category
from django.db import models
from django.contrib.auth.models import User

def update_filename(instance, filename):
    upload_to = 'uploads'
    instance.orig_name = filename
    ext = filename.split('.')[-1]
    filename = f"{uuid4().hex}.{ext}"
    return os.path.join(upload_to, filename)


# Create your models here.
class File(models.Model):
    orig_name = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True, null=True)
    path = models.FileField(upload_to=update_filename)
    dropbox_path = models.CharField(default="")
    category = models.CharField(max_length=255, blank=True)
    size = models.CharField(default="2Кб")
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

    def save(self, *args, **kwargs):
        if not self.category:  # Якщо категорія ще не визначена
            self.category = get_file_category(self.path.name)
        super().save(*args, **kwargs)