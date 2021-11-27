from backend.settings.base import *


DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'mann',
        'USER': 'mann',
        'PASSWORD': 'mann',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}
