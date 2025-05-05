from .base import *

DEBUG = False

ALLOWED_HOSTS = [
    h.strip() for h in os.getenv('ALLOWED_HOSTS', '').split(',') if h.strip()
]

CSRF_TRUSTED_ORIGINS = [
    h.strip() for h in os.getenv('CSRF_TRUSTED_ORIGINS', '').split(',') if h.strip()
]

SITE_DOMAIN = "https://www.fagnercalegario.com"

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True

SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
