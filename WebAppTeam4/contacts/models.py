from django.db import models
from django.contrib.auth.models import User
# Create your models here.
import datetime


class Contact (models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    birth_date = models.DateField()
    phone = models.CharField(max_length=16)
    email = models.EmailField()
    is_favorite = models.BooleanField(default=False)
    description = models.TextField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
