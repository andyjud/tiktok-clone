from django.urls import path
from .views import *

urlpatterns = [
    path('', messages, name="messages"),
    path('conversations/', conversations, name="conversations"),
    path('chat/<receiver_id>', chat, name="chat"),
    path('send_message/<receiver_id>', send_message, name="send_message"),
    path('delete_message/<message_id>', delete_message, name="delete_message"),
]