from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated

from utils.views import GenericViewSet

from goods.models import GoodsSKU

from . import serializers
from . import models


class OrderApi(mixins.ListModelMixin, mixins.CreateModelMixin, GenericViewSet):
    """订单模块"""
    queryset = models.OrderInfo.objects.all()
    permission_classes = [IsAuthenticated]
    route = {
        'list': serializers.OrderInfoReadModelSerializer,
        'create': serializers.OrderCreatSerializer,
    }

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def get_serializer_class(self):
        return self.route.get(self.action)


class PayOrderApi(mixins.CreateModelMixin, GenericViewSet):
    """请求支付"""
    serializer_class = serializers.OrderPaySerializer
    permission_classes = [IsAuthenticated]


class PayOrderCheckApi(mixins.CreateModelMixin, GenericViewSet):
    """查询是否支付成功!"""
    serializer_class = serializers.CheckOrderSerializer
    permission_classes = [IsAuthenticated]


class CommentApi(mixins.UpdateModelMixin, GenericViewSet):
    """更新评论接口,因为开始创建订单的时候评论默认为空,现在让用户修改,以后再修改还是这个put请求"""

    serializer_class = serializers.UpdateCommentModelSerializer

    queryset = models.OrderGoods.objects.all()

    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(order__user=self.request.user)
