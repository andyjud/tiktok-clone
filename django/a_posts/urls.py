from django.urls import path
from .views import *

urlpatterns = [
    path('', post_page_view),
    path('<pk>/', post_page_view, name='post_page'),
]
