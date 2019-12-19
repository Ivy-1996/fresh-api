from django.conf import settings
from django.core.files.storage import Storage

from .exceptions import OssOssStroageSaveFailError

import oss2

DEFAULT_ACCESS_KEY = getattr(settings, 'OSS_ACCESS_KEY', None)
DEFAULT_ACCESS_SECRET = getattr(settings, 'OSS_ACCESS_SECRET', None)
DEFAULT_ACCESS_BUCKET_NAME = getattr(settings, 'DEFAULT_ACCESS_BUCKET_NAME', None)
DEFAULT_ENDPOINT = getattr(settings, 'DEFAULT_ENDPOINT', None)


class OssStroage(oss2.Auth):

    def __init__(self, **kwargs):
        access_key = kwargs.get('access_key_id', DEFAULT_ACCESS_KEY)
        access_secret = kwargs.get('access_key_secret', DEFAULT_ACCESS_SECRET)
        assert all([access_key, access_secret]), 'access_key and access_secret can not be None'
        self.auth = super(OssStroage, self).__init__(**kwargs)

    def bucket(self, endpoint=None, bucket_name=None, *args, **kwargs):
        endpoint = endpoint or DEFAULT_ENDPOINT
        bucket_name = bucket_name or DEFAULT_ACCESS_BUCKET_NAME
        assert all([endpoint, bucket_name]), 'endpoint and bucket_name can not be None'
        return oss2.Bucket(self.auth, endpoint, bucket_name, *args, **kwargs)


class DjangoOssStroage(OssStroage, Storage):
    def _save(self, name, content):
        bucket = self.bucket()
        resp = bucket.put_object(name, content)
        if resp.status == 200:
            return resp.resp.response.url
        raise OssOssStroageSaveFailError(resp.resp)

    def exists(self, name):
        return False

    def url(self, name):
        return name
