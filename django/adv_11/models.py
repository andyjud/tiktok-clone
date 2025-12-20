from django.db import models
from django.conf import settings

class NotificationTracker(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="tracker")
    activity_last_seen = models.DateTimeField(null=True, blank=True)
