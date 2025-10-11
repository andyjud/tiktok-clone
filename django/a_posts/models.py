from django.db import models
from django.conf import settings
import uuid

class Post(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='posts')
    image = models.ImageField(upload_to='posts/')
    body = models.CharField(max_length=80, null=True, blank=True)
    tags = models.CharField(max_length=80, null=True, blank=True)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="likedposts", through="LikedPost")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at'] 
    
    def __str__(self):
        return str(self.uuid) 
    
    
class LikedPost(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at'] 
        unique_together = ('user', 'post')
