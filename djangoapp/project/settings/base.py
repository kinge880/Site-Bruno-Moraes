import os
from pathlib import Path
from django.contrib.messages import constants as message_constants

BASE_DIR = Path(__file__).resolve().parent.parent.parent

DATA_DIR = BASE_DIR.parent / 'data' / 'web'

SECRET_KEY = os.getenv('SECRET_KEY')

SHARED_APPS = [
    'django_tenants',
    'customers',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'public',
]

LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = '/'

TENANT_APPS = [
    'django.contrib.auth',
    'django.contrib.admin',
    'accounts',
    'bi',
    'shared',
]

INSTALLED_APPS = SHARED_APPS + TENANT_APPS

TENANT_MODEL = "customers.Cliente"
TENANT_DOMAIN_MODEL = "customers.Domain"

MIDDLEWARE = [
    'django_tenants.middleware.TenantMainMiddleware',
    'customers.middleware.ChecaPagamentoMiddleware',  # logo após o TenantMain
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]

AUTHENTICATION_BACKENDS = [
    'accounts.backends.EmailBackend',
]

ROOT_URLCONF = 'project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR , "templates")],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'project.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': os.getenv('DB_ENGINE'),
        'NAME': os.getenv('POSTGRES_DB'),
        'USER': os.getenv('POSTGRES_USER'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD'),
        'HOST': os.getenv('POSTGRES_HOST'),
        'PORT': os.getenv('POSTGRES_PORT'),
    }
}

DATABASE_ROUTERS = (
    'django_tenants.routers.TenantSyncRouter',
)

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Rio_Branco'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = DATA_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = DATA_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_REDIRECT_URL = '/meu-painel/'
LOGIN_URL = 'login'
LOGOUT_REDIRECT_URL = '/'
LOGOUT_URL = 'logout'

DATA_UPLOAD_MAX_MEMORY_SIZE = 50 * 1024 * 1024

MESSAGE_TAGS = {
    message_constants.DEBUG: 'debug',
    message_constants.INFO: 'info',
    message_constants.SUCCESS: 'success',
    message_constants.WARNING: 'warning',
    message_constants.ERROR: 'danger',
}

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://redis:6379/",
        "OPTIONS": {"CLIENT_CLASS": "django_redis.client.DefaultClient"},
        "KEY_PREFIX": "fagnercache"
    }
}

AUDITLOG_INCLUDE_ALL_MODELS = True

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.getenv('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = int(os.getenv('EMAIL_PORT', 587))
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS', 'True') == 'True'
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL')

ADMIN_SITE_HEADER = "Flow Hub"
ADMIN_SITE_TITLE = "Flow Hub Admin"
ADMIN_INDEX_TITLE = "Painel de Controle"
