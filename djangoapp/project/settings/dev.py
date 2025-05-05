from .base import *

DEBUG = True

ALLOWED_HOSTS = ['*']
CSRF_TRUSTED_ORIGINS = ['http://localhost', 'http://127.0.0.1']

SITE_DOMAIN = "http://localhost:8000"

STATICFILES_DIRS = [
    DATA_DIR / 'static',
]

SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
SECURE_SSL_REDIRECT = False
