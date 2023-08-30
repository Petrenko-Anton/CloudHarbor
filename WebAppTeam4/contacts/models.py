from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Contact (models.Model):
    name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    birth_date = models.DateField()
    phone = models.Charfield(max_length=16)
    email = models.EmailField()
    is_favorite = models.BooleanField(default=False)
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
