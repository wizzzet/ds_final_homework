from project.settings.__init__ import *  # NOQA

INSTALLED_APPS = list(INSTALLED_APPS)  # NOQA
i = 4
for app in (
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.admin'
):
    INSTALLED_APPS.insert(i, app)
    i += 1
INSTALLED_APPS = tuple(INSTALLED_APPS)


MIDDLEWARE = [
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware'
]

MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

ROOT_URLCONF = 'project.urls_admin'

DATA_UPLOAD_MAX_MEMORY_SIZE = 200 * 1024 * 1024
FILE_UPLOAD_MAX_MEMORY_SIZE = 200 * 1024 * 1024
DATA_UPLOAD_MAX_NUMBER_FIELDS = 10000

try:
    from project.settings.settings_local import *  # NOQA
except ImportError:
    pass

TEMPLATES[0]['OPTIONS']['debug'] = DEBUG  # NOQA
TEMPLATES[1]['OPTIONS']['cache_size'] = 1000000 if DEBUG else -1  # NOQA
TEMPLATES[1]['OPTIONS']['auto_reload'] = DEBUG  # NOQA
