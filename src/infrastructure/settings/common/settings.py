import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = '-@(f*76115chmgl4e)%u3=rmq83eyxo!@l)5*hppjd#4hzr7(j8'

DEBUG = True

ALLOWED_HOSTS = []

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'
