from .settings import *

DEBUG = False

# INSTALLED_APPS += ['debug_toolbar.apps.DebugToolbarConfig']
#
# MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']
#
# INTERNAL_IPS = ("127.0.0.1",)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'fresh_product',
        'USER': 'root',
        'PASSWORD': 'qwe123',
        'HOST': '127.0.0.1',
        'PORT': 3306,
    }
}
