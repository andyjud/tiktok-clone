from django.db import models
from django.contrib.auth.models import AbstractUser
from django.templatetags.static import static
from django_resized import ResizedImageField

class CustomUser(AbstractUser):
    name = models.CharField(max_length=30, null=True, blank=True)
    image = ResizedImageField(size=[600, 600], quality=75, upload_to='avatars/', null=True, blank=True)
    bio = models.TextField(blank=True, null=True)
    website = models.CharField(max_length=250, null=True, blank=True)
    birthday = models.DateField(blank=True, null=True)
    notifications = models.BooleanField(default=True)
    darkmode = models.BooleanField(default=False)
    
    def __str__(self):
        return self.username
    
    @property
    def avatar(self):
        if self.image:
            return self.image.url
        return static('images/avatar.svg')
    
    @property
    def website_link(self):
        if self.website and not self.website.startswith(('http://', 'https://')):
            return f'http://{self.website}'
        return self.website
