from .settings  import *

DEBUG = False

ALLOWED_HOSTS = ["5.183.9.86","mylifetravel.com.co","www.mylifetravel.com.co"]

CSRF_TRUSTED_ORIGINS = ['https://mylifetravel.com.co','https://www.mylifetravel.com.co']


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