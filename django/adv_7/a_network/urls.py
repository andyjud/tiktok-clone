from django.urls import path
from .views import *

urlpatterns = [
    path('user/<username>/', follow, name='follow'),
]