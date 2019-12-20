from rest_framework import views
from rest_framework import viewsets

from . import mixin
from .response import DefaultResponse


class BaseView:
    safe_response_status_code = [200, 201, 202, 203, 204, 400]
    success_status_code = [200, 201, 202, 203, 204]
    fail_status_code = [400]
    success_handle = 'get_success_handle'
    fail_handle = 'get_fail_handle'

    def get_default_response(self, request, response, *args, **kwargs):
        if self.is_safe_response(response):
            status_code = response.status_code
            source = self.success_handle if status_code in self.success_status_code else self.fail_handle
            response = getattr(self, source)(request, response, *args, **kwargs)
        return response

    def is_safe_response(self, response):
        return response.status_code in self.safe_response_status_code

    def get_success_handle(self, request, response, *args, **kwargs):
        raise NotImplementedError()

    def get_fail_handle(self, request, response, *args, **kwargs):
        raise NotImplementedError()


class ApiView(DefaultResponse, BaseView, mixin.ApiViewMinxin, views.APIView):
    pass


class GenericViewSet(DefaultResponse, BaseView, mixin.ViewSetMixIn, viewsets.GenericViewSet):
    pass


class ReadOnlyModelViewSet(DefaultResponse, BaseView, mixin.ViewSetMixIn, viewsets.ReadOnlyModelViewSet):
    pass


class ModelViewSet(DefaultResponse, BaseView, mixin.ViewSetMixIn, viewsets.ModelViewSet):
    pass


def exception_handler(exc, context):
    pass
