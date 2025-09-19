from django.urls import path
from .views import profile_view, profile_edit, verification_code

urlpatterns = [
    path('', profile_view),
    path('edit/', profile_edit, name='profile_edit'),
    path('verification_code/', verification_code, name='verification_code'),
]
