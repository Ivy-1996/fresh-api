from .settings import *

DEBUG = False

INSTALLED_APPS += ['debug_toolbar.apps.DebugToolbarConfig']

MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']

INTERNAL_IPS = ("127.0.0.1",)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': '',
        'USER': '',
        'PASSWORD': '',
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

# nginx代理的FastDfs域名
IMAGE_DOMAIN = 'http://img.summerleaves.cn/'

# 支付宝的app_id
ALIPAY_APP_ID = ''

# 支付宝私钥
APP_PRIVATE_KEY_PATH = os.path.join(BASE_DIR, 'conf/app_private_key.pem')

# 支付宝公钥
ALIPAY_PUBLIC_KEY_PATH = os.path.join(BASE_DIR, 'conf/alipay_public_key.pem')
