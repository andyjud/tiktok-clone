INSTALLED_APPS = [   
    # My apps
    'a_posts',
    
    # Third party
    'django_browser_reload',
]

MIDDLEWARE = [
    'django_htmx.middleware.HtmxMiddleware',
]
if DEBUG:
    MIDDLEWARE += ['django_browser_reload.middleware.BrowserReloadMiddleware']


STATIC_URL = 'static/'
STATICFILES_DIRS = [ BASE_DIR / "static" ]

MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / "media"

AUTH_USER_MODEL = 'a_users.CustomUser'
