from django.core.files.storage import Storage
from django.conf import settings

from .exceptions import OssOssStroageSaveFailError

import oss2
from fdfs_client.client import Fdfs_client

DEFAULT_ACCESS_KEY = getattr(settings, 'OSS_ACCESS_KEY', None)
DEFAULT_ACCESS_SECRET = getattr(settings, 'OSS_ACCESS_SECRET', None)
DEFAULT_ACCESS_BUCKET_NAME = getattr(settings, 'DEFAULT_ACCESS_BUCKET_NAME', None)
DEFAULT_ENDPOINT = getattr(settings, 'DEFAULT_ENDPOINT', None)
IMAGE_DOMAIN = getattr(settings, 'IMAGE_DOMAIN', None)
FDFS_CLIENT_CONF = getattr(settings, 'FDFS_CLIENT_CONF', None)


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


class FdfsStorage(Storage):
    default_client = FDFS_CLIENT_CONF
    default_image_domain = IMAGE_DOMAIN

    def __init__(self, client=None, img_domain=None):
        self.client = client or self.default_client
        self.img_domain = img_domain or self.default_image_domain
        assert self.client is not None, 'clien path can not be None' \
                                        'you can set global `FDFS_CLIENT_CONF` in your setting'
        assert self.img_domain is not None, 'img_domain can not be None' \
                                            'you can set global `IMAGE_DOMAIN` in your setting'

    def _save(self, name, content):
        client = Fdfs_client(self.client)
        response = client.upload_by_buffer(content.read())
        if response.get('Status') != 'Upload successed.':
            raise Exception('upload to fdfs failed')
        filename = response.get('Remote file_id')
        return filename

    def exists(self, name):
        return False

    def url(self, name):
        return self.img_domain + name
