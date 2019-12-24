from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import mixins

from django_redis import get_redis_connection

from utils.views import GenericViewSet

from goods.models import GoodsSKU

from . import serializers
from . import permission


# 这几个模块分来来做要比放在一个ViewSet中要方便

class AddCartApi(mixins.CreateModelMixin, GenericViewSet):
    """添加购物车"""
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.AddCartSerializer


class CartInfoApi(GenericViewSet):
    """购物车详情"""
    # 这里不在类属性中定义`serializers_class`,免得被api文档捕捉到,造成误读
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


class UpdateCartApi(mixins.UpdateModelMixin, GenericViewSet):
    """更新购物车"""
    permission_classes = [IsAuthenticated, permission.HasCartSkuPermission]
    serializer_class = serializers.UpdateCartSerializer
    queryset = GoodsSKU.objects.filter(is_delete=False)


class DeleteCartApi(GenericViewSet):
    """删除购物车"""
    permission_classes = [IsAuthenticated, permission.HasCartSkuPermission]
    queryset = GoodsSKU.objects.filter(is_delete=False)

    def destroy(self, request, *args, **kwargs):
        # 主要是为了校验权限
        self.get_object()
        coon = get_redis_connection('default')
        cart_key = 'cart_%d' % request.user.pk
        pk = kwargs.get('pk')
        coon.hdel(cart_key, pk)
        return Response({'msg': '删除成功!'})
