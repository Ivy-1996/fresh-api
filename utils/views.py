from django.conf import settings
from django.utils.module_loading import import_string

from rest_framework import views
from rest_framework import viewsets
from rest_framework.response import Response

from . import mixin
from .response import DefaultResponse

DRF_SETTINGS = getattr(settings, 'REST_FRAMEWORK', dict())


##############################################################
# 将你的代码继承这些类,可以达到不修改原来的代码完成处理请求结果的定制化 #
##############################################################


class APIView(DefaultResponse, mixin.ApiViewMinxin, views.APIView):
    pass


class GenericViewSet(DefaultResponse, mixin.ViewSetMixIn, viewsets.GenericViewSet):
    pass


class ReadOnlyModelViewSet(DefaultResponse, mixin.ViewSetMixIn, viewsets.ReadOnlyModelViewSet):
    pass


class ModelViewSet(DefaultResponse, mixin.ViewSetMixIn, viewsets.ModelViewSet):
    pass


# 默认处理框架返回的错误信息
class BaseExceptionHandle:
    def __init__(self, ext, context, *args, **kwargs):
        self.ext = ext
        self.context = context
        # 获取框架的处理结果
        self.response = views.exception_handler(self.ext, self.context)

    def dispatch(self):
        # 默认行为为根据响应的状态码来分发请求
        # 如果要定制,请重写该方法
        handle = getattr(self, f'dispatch_{self.response.status_code}', self.default_response)
        return handle()

    def default_response(self):
        return self.response

    def __call__(self, *args, **kwargs):
        return self.dispatch()


class DefaultExceptionHandle(BaseExceptionHandle):
    def dispatch_404(self):
        # 没有结果不想返回404
        response = {'success': True, 'results': []}
        return Response(response)


exception_handle = DRF_SETTINGS.get('DEFAULT_EXCEPTION_HANDLE_CLASS', 'rest_framework.views.exception_handler')

EXCEPTION_HANDLE = import_string(exception_handle)


# 错误请求的处理函数
def exception_handler(exc, context):
    # 去全局配置里面
    response = EXCEPTION_HANDLE(exc, context)
    return response() if callable(response) else response
