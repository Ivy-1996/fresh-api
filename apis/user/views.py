from django.contrib.auth import get_user_model

from utils.views import GenericViewSet
from rest_framework import mixins
from . import serializers


# 注册模块
class RegisterApi(mixins.CreateModelMixin, GenericViewSet):
    serializer_class = serializers.RegisterSerializer


# 登录模块
class LoginApi(mixins.CreateModelMixin, GenericViewSet):
    serializer_class = serializers.LoginSerializer
