from rest_framework.permissions import IsAuthenticated
from rest_framework import mixins

from django_redis import get_redis_connection
from rest_framework.response import Response

from utils.views import GenericViewSet

from . import serializers


class AddCartApi(mixins.CreateModelMixin, GenericViewSet):
    """添加购物车"""
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.AddCartSerializer


class CartInfoApi(GenericViewSet):
    """购物车详情"""
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        user = request.user
        coon = get_redis_connection('default')
        cart_key = 'cart_%d' % user.id
        # 获取所有的购物车信息
        cart_dict = coon.hgetall(cart_key)
        # 将byte字典转换为int字典
        cart = {int(key): int(value) for key, value in cart_dict.items()}
        data = {'cart': cart}
        # 交给序列化器处理
        serializer = serializers.CartInfoSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)
