import datetime
import os


def gettext_noop(s):
    return s


PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE_ROOT = os.path.dirname(PROJECT_DIR)

ENV = 'production'
DEBUG = True

ADMINS = (
    ('Rafael Kamashev', 'wizzzet@gmail.com'),
)
MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'stack_exchange_faq',
        'USER': 'stack_exchange_faq',
        'PASSWORD': 'stack_exchange_faq',
        'HOST': 'localhost',
        'PORT': '5433'
    }
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

TIME_ZONE = 'UTC'
LANGUAGE_CODE = 'ru'
LANGUAGES = (
    ('ru', gettext_noop('Russian')),
    # ('en', gettext_noop('English'))
)
LANGUAGE_CODES = tuple([x[0] for x in LANGUAGES])
LANGUAGE_CODES_PUBLIC = ('ru',)  # 'en'
DEFAULT_LANGUAGE = LANGUAGES[0][0]

SITE_ID = 1
SITE_NAME = 'ask.wizzzet.ru'
SITE_PROTOCOL = 'https://'

USE_I18N = True
USE_L10N = True
USE_TZ = True

MEDIA_ROOT = os.path.normpath(os.path.join(SITE_ROOT, 'public', 'media'))
MEDIA_URL = '/media/'

STATIC_ROOT = os.path.normpath(os.path.join(SITE_ROOT, 'public', 'static'))
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.normpath(os.path.join(SITE_ROOT, 'static')),
)
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder'
)

LOCALE_PATHS = (
    os.path.normpath(os.path.join(SITE_ROOT, 'locale')),
)

SECRET_KEY = r'*94xc1v)usc!er=ly8@9)%^+c=esbv)u2sc!uo:oy8@9dy@c3orj5o++#!qcq5'

template_context_processors = (
    'django.contrib.auth.context_processors.auth',
    'django.template.context_processors.debug',
    'django.template.context_processors.i18n',
    'django.template.context_processors.media',
    'django.template.context_processors.static',
    'django.template.context_processors.tz',
    'django.contrib.messages.context_processors.messages',
    'django.template.context_processors.request'
)
TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [
        os.path.join(SITE_ROOT, 'templates'),
    ],
    'OPTIONS': {
        'context_processors': template_context_processors,
        'debug': DEBUG,
        'loaders': (
            (
                'django.template.loaders.cached.Loader',
                (
                    'django.template.loaders.filesystem.Loader',
                    'django.template.loaders.app_directories.Loader'
                )
            ),
        )
    }
}, {
    'BACKEND': 'django.template.backends.jinja2.Jinja2',
    'DIRS': [
        os.path.join(SITE_ROOT, 'templates'),
    ],
    'APP_DIRS': True,
    'OPTIONS': {
        'autoescape': False,
        'cache_size': 1000000 if DEBUG else -1,
        'auto_reload': DEBUG,
        'environment': 'snippets.template_backends.jinja2.environment',
        'extensions': ('jinja2.ext.i18n',)
    }
}]

MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

MIDDLEWARE = [
    'snippets.middlewares.language.LanguageMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware'
]

ROOT_URLCONF = 'project.urls'

INSTALLED_APPS = (
    'corsheaders',
    'django.contrib.auth',
    'django.contrib.sites',
    'django.contrib.contenttypes',
    'django.contrib.staticfiles',
    'django.contrib.postgres',
    'django_celery_results',
    'rest_framework',
    'drf_yasg',
    'import_export',
    'exchange',
    'users'
)

API_APPS = (
    # 'exchange',
)

LOGIN_REDIRECT_URL = '/'
LOGIN_ALWAYS_REQUIRED = False
# url, которые игнорируются при проверке входа
LOGIN_EXEMPT_URLS = (r'^media/.*', '^static/.*')

AUTH_USER_MODEL = 'users.User'
AUTHENTICATION_BACKENDS = ('django.contrib.auth.backends.ModelBackend',)

DATE_FORMAT = 'd.m.Y'
DATETIME_FORMAT = 'd.m.Y H:i:s'
DATE_INPUT_FORMATS = (
    '%Y-%m-%d',
    '%d.%m.%Y'
)
DATETIME_INPUT_FORMATS = (
    '%Y-%m-%d %H:%M:%S',     # '2006-10-25 14:30:59'
    '%Y-%m-%dT%H:%M:%S',
    '%Y-%m-%d %H:%M:%S.%f',  # '2006-10-25 14:30:59.000200'
    '%Y-%m-%d %H:%M',        # '2006-10-25 14:30'
    '%Y-%m-%d',              # '2006-10-25'
    '%m/%d/%Y %H:%M:%S',     # '10/25/2006 14:30:59'
    '%m/%d/%Y %H:%M:%S.%f',  # '10/25/2006 14:30:59.000200'
    '%m/%d/%Y %H:%M',        # '10/25/2006 14:30'
    '%m/%d/%Y',              # '10/25/2006'
    '%m/%d/%y %H:%M:%S',     # '10/25/06 14:30:59'
    '%m/%d/%y %H:%M:%S.%f',  # '10/25/06 14:30:59.000200'
    '%m/%d/%y %H:%M',        # '10/25/06 14:30'
    '%m/%d/%y',              # '10/25/06'
    '%d.%m.%Y %H:%M:%S',
    '%d.%m.%Y %H:%M'
)

DEFAULT_FROM_EMAIL = 'robot@%s' % SITE_NAME
EMAIL_BATCH_SIZE = 100

REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_DB = 1

CACHES = {
    'default': {
        'BACKEND': 'redis_cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/2',
        'OPTIONS': {
            'DB': 2,
            'PARSER_CLASS': 'redis.connection.HiredisParser',
            'CONNECTION_POOL_CLASS': 'redis.BlockingConnectionPool',
            'CONNECTION_POOL_CLASS_KWARGS': {
                'max_connections': 150,
                'timeout': 20,
            },
            'MAX_CONNECTIONS': 1000,
            'CLIENT_CLASS': 'django_redis.client.DefaultClient'
        }
    }
}
CACHE_PAGE_TIMEOUT = 60

CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'django-db'
CELERY_TASK_RESULT_EXPIRES = 3600
CELERY_TIMEZONE = 'UTC'
CELERY_ENABLE_UTC = True

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny',
        'rest_framework.permissions.IsAuthenticated'
    ),
    'DEFAULT_PAGINATION_CLASS':
        'rest_framework.pagination.LimitOffsetPagination',
    'UPLOADED_FILES_USE_URL': False,
    'PAGE_SIZE': 10,
    'DATE_INPUT_FORMATS': DATE_INPUT_FORMATS
}

SWAGGER_SETTINGS = {
    'DEFAULT_AUTO_SCHEMA_CLASS': 'core.schema.ProjectSwaggerAutoSchema',
    'DEFAULT_INFO': 'project.urls.api_info',
    'SECURITY_DEFINITIONS': {
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
        }
    }
}

JWT_AUTH = {
    'JWT_ALGORITHM': 'HS512',
    'JWT_ALLOW_REFRESH': True,
    'JWT_AUTH_HEADER_PREFIX': 'Bearer',
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=30),
    'JWT_LEEWAY': 30,
    'JWT_REFRESH_EXPIRATION_DELTA': datetime.timedelta(days=30),
    'JWT_SECRET_KEY': SECRET_KEY[:],
    'JWT_VERIFY': True,
    'JWT_VERIFY_EXPIRATION': True,
    'JWT_VERIFY_IAT': True,
    'JWT_RESPONSE_PAYLOAD_HANDLER':
        'snippets.api.auth.jwt_response_payload_handler'
}

DATA_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024

try:
    from project.settings.local_settings import *  # NOQA
except ImportError:
    pass


SITE_URL = SITE_PROTOCOL + SITE_NAME
API_BASE_URL = f'{SITE_URL}/api/'
CSRF_TRUSTED_ORIGINS = [f'{x}{SITE_NAME}' for x in ('https://', 'http://')]

TEMPLATES[0]['OPTIONS']['debug'] = DEBUG
TEMPLATES[1]['OPTIONS']['cache_size'] = 1000000 if DEBUG else -1
TEMPLATES[1]['OPTIONS']['auto_reload'] = DEBUG

CORS_ORIGIN_ALLOW_ALL = DEBUG
