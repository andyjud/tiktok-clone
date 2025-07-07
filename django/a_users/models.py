from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    name = models.CharField(max_length=30, null=True, blank=True)
    image = models.ImageField(upload_to='avatars/', null=True, blank=True)
    bio = models.TextField(blank=True, null=True)
    birthday = models.DateField(blank=True, null=True)
    
    def __str__(self):
        return self.username
