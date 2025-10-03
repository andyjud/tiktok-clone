from django.contrib import admin
from django.urls import path, include, reverse_lazy
from django.conf import settings
from django.conf.urls.static import static
from allauth.account.views import PasswordChangeView
from a_posts.views import *
from a_users.views import profile_view, index_view

urlpatterns = [
    path('', home_view, name="home"),
    path('admin/', admin.site.urls),
    path("accounts/password/change/", PasswordChangeView.as_view(success_url=reverse_lazy("settings")), name="account_change_password"),
    path('accounts/', include('allauth.urls')),
    path('login/', index_view, name="index"),
    path('@<username>/', profile_view, name="profile"),
    path('explore/', explore_view, name="explore"),
    path('upload/', upload_view, name="upload"),
    path('post/', include("a_posts.urls")),
    path('profile/', include("a_users.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += [
        path("__reload__/", include("django_browser_reload.urls")),
    ]
