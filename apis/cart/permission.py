from rest_framework.permissions import BasePermission

from django_redis import get_redis_connection


class HasCartSkuPermission(BasePermission):
    # 校验当前用户的购物车中是否有该物品
    def has_object_permission(self, request, view, obj):
        cart_key = 'cart_%d' % request.user.pk
        coon = get_redis_connection('default')
        return coon.hexists(cart_key, obj.pk)
