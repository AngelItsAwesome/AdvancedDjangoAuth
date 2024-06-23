from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class CustomUser(AbstractUser):
    email = models.EmailField(max_length=100)
    celphone = models.CharField(max_length=15, default='', null=False)
    verified = models.BooleanField(default=False)
    token = models.CharField(max_length=100, default='')

    def __str__(self):
        return self.username

