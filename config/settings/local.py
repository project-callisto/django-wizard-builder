from .base import *

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'crapllisto',
        'USER': 'work',
        'PASSWORD': '',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}


STATIC_URL = '/static/'
STATIC_ROOT = os.path.abspath(os.path.join(BASE_DIR, '../../static'))

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
        },
    },
    'root': {'level': 'INFO'},
}

BOOTSTRAP3 = {

    # The URL to the jQuery JavaScript file
    'jquery_url': '/static/js/jquery.min.js',

    #    # The complete URL to the Bootstrap CSS file (None means derive it from base_url)
    'css_url': '/static/bootstrap/css/bootstrap.min.css',

    # The complete URL to the Bootstrap CSS file (None means no theme)
    'theme_url': '/static/bootstrap/css/bootstrap-theme.min.css',

    # The complete URL to the Bootstrap JavaScript file (None means derive it from base_url)
    'javascript_url': '/static/bootstrap/js/bootstrap.min.js',
}