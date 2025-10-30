from django.urls import path
from .views import *

urlpatterns = [
    path('', post_page_view),
    path('<pk>/', post_page_view, name='post_page'),
    path('post_edit/<pk>/', post_edit, name='post_edit'),
    path('like/<pk>/', like_post, name='like_post'),
    path('bookmark/<pk>/', bookmark_post, name='bookmark_post'),
    path('comment/<pk>/', comment, name='comment'),
    path('comment_delete/<pk>/', comment_delete, name='comment_delete'),
    path('like_comment/<pk>/', like_comment, name='like_comment'),
]
