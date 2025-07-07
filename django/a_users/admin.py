from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('name', 'image', 'bio', 'birthday')}),    
    ) + UserAdmin.fieldsets # type: ignore
    list_display = ('username', 'name', 'email', 'is_staff')