from django.db import models
from django.conf import settings

class Conversation(models.Model):
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, through="ConvUser", related_name="conversations")
    updated_at = models.DateTimeField(auto_now=True)
    
class ConvUser(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    unread_count = models.IntegerField(default=0)
    last_seen_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        unique_together = ("conversation", "user")
        
class Message(models.Model):
    conversation = models.ForeignKey(Conversation, related_name="messages", on_delete=models.CASCADE)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    body = models.TextField()
    image = models.ImageField(upload_to="chat_images/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    @property
    def emoji_only(self):
        message = self.body.strip()
        for character in message:
            if character.isalnum():
                return False
        return True
