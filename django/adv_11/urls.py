from django.urls import path
from .views import *

urlpatterns = [
    path('', notifications, name="notifications"),
    path("new_notifications/", new_notifications, name="new_notifications"),
]