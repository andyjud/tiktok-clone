from django.contrib import admin
from .models import Post, LikedPost, BookmarkedPost

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'author', 'body')
    
    
@admin.register(LikedPost)
class LikedPostAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'user', 'post')
    
    
@admin.register(BookmarkedPost)
class BookmarkedPostAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'user', 'post')
