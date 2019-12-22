from rest_framework import serializers
from rest_framework.utils.serializer_helpers import ReturnDict

from django_redis import get_redis_connection

from goods.models import GoodsSKU
from goods.serializers import GoodsSkuModelSerializer


class AddCartSerializer(serializers.Serializer):
    sku = serializers.PrimaryKeyRelatedField(queryset=GoodsSKU.objects.all())
    count = serializers.IntegerField()

    # 校验商品数目的合法性
    def validate_count(self, attr):
        if attr > 0:
            return attr
        raise serializers.ValidationError({'count': ['商品的数目必须大于0']})

    # 校验库存
    def validate(self, attrs):
        count = attrs.get('count')
        sku = attrs.get('sku')
        if count > sku.stock:
            raise serializers.ValidationError({'count': ['商品的库存不足']})
        return attrs

    # 加入购物车保存
    def save(self, **kwargs):
        coon = get_redis_connection('default')
        user = self.context.get('request').user
        cart_key = 'cart_%d' % user.pk
        # 获取购物车中该物品的数目
        sku = self.validated_data.get('sku')
        count = self.validated_data.get('count')
        cart_count = coon.hget(cart_key, sku.pk) or 0
        cart_count = int(cart_count) + count
        # 加入购物车
        coon.hset(cart_key, sku.pk, cart_count)

    # 返回应答
    @property
    def data(self):
        coon = get_redis_connection('default')
        user = self.context.get('request').user
        cart_key = 'cart_%d' % user.pk
        # 获取购物车中的sku的数目
        cart_count = coon.hlen(cart_key)
        return ReturnDict({'cart_count': cart_count, 'msg': '添加成功!'}, serializer=self)


class CartInfoSerializer(serializers.Serializer):
    cart = serializers.DictField()

    # 转换cart
    def validate_cart(self, attrs):
        resp = list()
        for pk, count in attrs.items():
            item = dict()
            # try:
            #     GoodsSKU.objects.get(pk=pk)
            # except GoodsSKU.DoesNotExist:
            #     raise serializers.ValidationError({'cart': ['商品不存在!']})
            sku = GoodsSKU.objects.get(pk=pk)
            item['sku'] = sku
            item['count'] = count
            resp.append(item)
        return resp

    @property
    def data(self):
        total_count = 0
        total_price = 0
        resp = list()
        # 获取购物车信息
        cart = self.validated_data.get('cart')
        for each in cart:
            item = dict()
            sku = each.get('sku')
            count = each.get('count')
            # 获取sku的信息
            serializer = GoodsSkuModelSerializer(instance=sku)
            # 计算当前sku的小计
            amount = sku.price * count
            # 计算总数目
            total_count += count
            # 计算总价格
            total_price += amount
            # 存储信息
            item['sku'] = serializer.data
            item['count'] = count
            item['amount'] = amount
            resp.append(item)
        # 格式化信息
        response = {
            'total_count': total_price,
            'total_price': total_price,
            'item': resp
        }
        # 返回应答
        return ReturnDict(response, serializer=self)
