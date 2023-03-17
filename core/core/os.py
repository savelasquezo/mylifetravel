from .settings  import *

DEBUG = False

ALLOWED_HOSTS = ["5.183.9.86","mylifetravel.com.co","www.mylifetravel.com.co"]

CSRF_TRUSTED_ORIGINS = ['https://mylifetravel.com.co','https://www.mylifetravel.com.co']

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.hostinger.com'
EMAIL_PORT = 465
EMAIL_USE_SSL = True
EMAIL_HOST_USER = 'noreply@mylifetravel.com.co'
EMAIL_HOST_PASSWORD = 'hRjW6#R!@37P1'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'dbmylifetravel',
        'USER': 'postgres',
        'PASSWORD': 'hRjW6#R!@37P1',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': '/home/app/mylifetravel/core/logs/django.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}