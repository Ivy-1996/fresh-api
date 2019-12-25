from .settings import *

DEBUG = True

INSTALLED_APPS += ['debug_toolbar.apps.DebugToolbarConfig']

MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']

INTERNAL_IPS = ("127.0.0.1",)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'fresh_develop',
        'USER': 'root',
        'PASSWORD': 'qwe123',
        'HOST': '127.0.0.1',
        'PORT': 3306,
    }
}

BROKER = 'redis://127.0.0.1:6379/3'

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": 'redis://127.0.0.1:6379/0',
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
    "session": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": 'redis://127.0.0.1:6379/1',
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
}

IMAGE_DOMAIN = 'http://img.summerleaves.cn/'

ALIPAY_APP_ID = '2016101300674998'

APP_PRIVATE_KEY_PATH = os.path.join(BASE_DIR, 'conf/app_private_key.pem')

ALIPAY_PUBLIC_KEY_PATH = os.path.join(BASE_DIR, 'conf/alipay_public_key.pem')
