from django.contrib.auth import get_user_model, logout

from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import mixins

from django_redis import get_redis_connection

from utils.views import GenericViewSet, ModelViewSet

from goods.serializers import GoodsSkuModelSerializer

from . import serializers
from . import models


class RegisterApi(mixins.CreateModelMixin, GenericViewSet):
    """注册模块"""
    serializer_class = serializers.RegisterSerializer


class LoginApi(mixins.CreateModelMixin, GenericViewSet):
    """登录模块"""
    serializer_class = serializers.LoginSerializer


class LougoutApi(GenericViewSet):
    """退出模块"""

    def list(self, request, *args, **kwargs):
        print(request.user)
        logout(request)
        return Response({'msg': '退出成功!'})


class UserActiveApi(GenericViewSet):
    """用户激活模块"""
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
        # 获取用户,将状态设置为True
        user = get_user_model().objects.get(pk=pk)
        user.is_active = True
        user.save()
        return Response({'msg': '激活成功!'})


class AddressApi(ModelViewSet):
    """用户收货地址接口"""
    permission_classes = [IsAuthenticated]
    queryset = models.Address.objects.all()
    serializer_class = serializers.AddressModelSerializer
    filterset_fields = ['is_default']


class HistoryApi(mixins.ListModelMixin, GenericViewSet):
    """用户的历史浏览记录"""
    permission_classes = [IsAuthenticated]
    queryset = serializers.GoodsSKU.objects.all()

    # 重写`list`设置`serializer_class`,而不是重写`get_serializer_class`,这样可以不会被api文档捕捉到,造成误读
    def list(self, request, *args, **kwargs):
        self.serializer_class = GoodsSkuModelSerializer
        return super().list(request, *args, **kwargs)

    # 将用户的历史浏览记录转换为`queryset`对象返回给`ListModelMixin`
    def filter_queryset(self, queryset):
        # 获取用户的历史浏览记录
        coon = get_redis_connection('default')
        history_key = 'history_%d' % self.request.user.pk
        histories = coon.lrange(history_key, 0, 4)
        # byte转int
        histories = [int(pk) for pk in histories]
        data = {'histories': histories}
        # 序列化,返回`queryset`
        serializer = serializers.HistorySerializer(data=data)
        serializer.is_valid(raise_exception=True)
        return serializer.validated_data
