from src.infrastructure.settings.common.settings import *


WSGI_APPLICATION = 'src.infrastructure.settings.django.sqlite.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': str(f'{BASE_DIR.parent}/database/sqlite/db.sqlite3'),
    }
}

ROOT_URLCONF = 'src.infrastructure.settings.common.urls'
