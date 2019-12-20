from django.contrib.auth import get_user_model, logout
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from utils.views import GenericViewSet, ApiView, ModelViewSet
from rest_framework import mixins
from . import serializers
from . import models


class RegisterApi(mixins.CreateModelMixin, GenericViewSet):
    # 注册模块
    serializer_class = serializers.RegisterSerializer


class LoginApi(mixins.CreateModelMixin, GenericViewSet):
    # 登录模块
    serializer_class = serializers.LoginSerializer


class LougoutApi(GenericViewSet):
    # 退出模块
    def list(self, request, *args, **kwargs):
        print(request.user)
        logout(request)
        return Response({'msg': '退出成功!'})


class UserActiveApi(GenericViewSet):
    # 用户激活模块
    serializer_class = serializers.UserActiveSerializer
    lookup_field = 'token'
    # 设置查找方式为所有
    lookup_value_regex = '.*'

    def retrieve(self, request, *args, **kwargs):
        # 拿到url中的参数验证合法性
        serializer = self.get_serializer(data=kwargs)
        serializer.is_valid(raise_exception=True)
        # 将用户激活
        data = serializer.validated_data
        pk = data.get('user')
        user = get_user_model().objects.get(pk=pk)
        user.is_active = True
        user.save()
        return Response({'msg': '激活成功!'})


class AddressApi(ModelViewSet):
    # 用户收货地址接口
    permission_classes = [IsAuthenticated]
    queryset = models.Address.objects.all()
    serializer_class = serializers.AddressModelSerializer
