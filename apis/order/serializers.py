from django.db import transaction
from django.conf import settings

from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.utils.serializer_helpers import ReturnDict

from django_redis import get_redis_connection

from alipay import AliPay

from datetime import datetime

from goods.models import GoodsSKU
from user.models import Address

from . import models


class OrderGoodsModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.OrderGoods
        fields = '__all__'


class OrderInfoReadModelSerializer(serializers.ModelSerializer):
    # 查询该订单的所有的商品
    goods = serializers.ManyRelatedField(OrderGoodsModelSerializer(), source='ordergoods_set')

    class Meta:
        model = models.OrderInfo
        fields = '__all__'


class OrderCreatSerializer(serializers.Serializer):
    skus = serializers.ListField(child=serializers.PrimaryKeyRelatedField(queryset=GoodsSKU.objects.all()))
    addr = serializers.PrimaryKeyRelatedField(queryset=Address.objects.all())
    pay_method = serializers.CharField()

    # 校验支付方式的合法性
    def validate_pay_method(self, attrs):
        if attrs not in models.OrderInfo.PAY_METHODS.keys():
            raise serializers.ValidationError({'pay_method': ['请选择合法的支付方式']})
        return attrs

    # 校验地址是否为用户的
    def validate_addr(self, attrs):
        user = self.context.get('request').user
        if attrs.user.id != user.id:
            raise serializers.ValidationError({'addr': ['非法的地址id']})
        return attrs

    # 校验商品是否都在用户的购物车中
    def validate_skus(self, attrs):
        user = self.context.get('request').user
        coon = get_redis_connection('default')
        key = 'cart_%d' % user.id
        cart_data = coon.hgetall(key)
        cart_key = [int(key) for key in cart_data.keys()]
        # 这里的商品的合法性序列化器已经校验过了,我们只用校验它是否在购物车中即可
        # 取出原始的数据
        skus_raw_data = self.initial_data.get('skus')
        if skus_raw_data != cart_key:
            raise serializers.ValidationError({'skus': ['非法的请求']})
        return attrs

    # 创建订单
    @transaction.atomic
    def create(self, validated_data):
        # 设置保存点
        save_point = transaction.savepoint()
        addr = validated_data.get('addr')
        pay_method = validated_data.get('pay_method')
        skus = validated_data.get('skus')
        user = self.context.get('request').user
        coon = get_redis_connection('default')
        cart_key = 'cart_%d' % user.id
        # 运费假数据,先死,这个可以根据用户的地址和商品的规格来计算运费,这里直接先写死
        transit_price = 10
        total_count = 0
        total_price = 0
        order_id = datetime.now().strftime('%Y%m%d%H%M%S') + str(user.id)
        try:

            # 创建订单
            order = models.OrderInfo.objects.create(
                order_id=order_id,
                user=user,
                addr=addr,
                pay_method=pay_method,
                total_count=total_count,
                total_price=total_price,
                transit_price=transit_price
            )
            for sku in skus:
                # 这里上面已经校验过了,这里再拿一次主要是为了加锁
                # 也可以设置mysql数据库的事物的隔离级别为`serializable`,这样可以就不用了重复查询了
                sku = GoodsSKU.objects.select_for_update().get(id=sku.id)
                # 为了避免错误,这里加上一个0
                count = int(coon.hget(cart_key, sku.id) or 0)

                # 再来判断一次库存
                if count > sku.stock:
                    transaction.savepoint_rollback(save_point)
                    return Response({'errmsg': '商品的库存不足!'})

                # 创建订单商品
                models.OrderGoods.objects.create(
                    order=order,
                    sku=sku,
                    count=count,
                    price=sku.price,
                )
                # 商品属性变动
                sku.stock -= int(count)
                sku.sales += int(count)
                sku.save()

                # 计算小计
                amount = sku.price * int(count)
                total_count += int(count)
                total_price += amount

            # 修改之前的order订单信息
            order.total_count = total_count
            order.total_price = total_price
            order.save()
        except Exception as e:
            print(e)
            # 可能数据库错误,下单失败
            transaction.savepoint_rollback(save_point)
            raise serializers.ValidationError({'errmsg': '下单失败'})

        # 提交事物
        transaction.savepoint_commit(save_point)

        # 清空购物车
        skus_raw_data = self.initial_data.get('skus')
        coon.hdel(cart_key, *skus_raw_data)
        return validated_data

    # 返回应答
    @property
    def data(self):
        return ReturnDict({'msg': '创建成功!'}, serializer=self)


# 创建抽象的基类
class AbstractPaySerializer(serializers.Serializer):
    order = serializers.CharField(max_length=30)

    def validate(self, attrs):
        order_id = attrs.get('order')
        user = self.context.get('request').user
        # 校验订单和当前用户的归属关系
        try:
            order = models.OrderInfo.objects.get(order_id=order_id, user=user)
        except models.OrderInfo.DoesNotExist:
            raise serializers.ValidationError({'order': ['订单不存在']})

        # 校验支付方式
        # 当前仅支持支付宝!
        if order.pay_method != 3:
            return Response({'errmsg': '目前仅支持支付宝支付!'})
        return order

    @property
    def alipay(self):
        alipay = AliPay(
            appid=settings.ALIPAY_APP_ID,
            app_notify_url=None,  # 默认回调url
            app_private_key_path=settings.APP_PRIVATE_KEY_PATH,
            # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            alipay_public_key_path=settings.ALIPAY_PUBLIC_KEY_PATH,
            sign_type="RSA2",  # RSA 或者 RSA2
            debug=True  # 默认False
        )
        return alipay


# 支付请求
class OrderPaySerializer(AbstractPaySerializer):

    # 对接支付宝
    # 获取支付的url
    def save(self, **kwargs):
        order = self.validated_data
        order_id = order.order_id
        alipay = self.alipay
        total_pay = order.total_price + order.transit_price

        order_string = alipay.api_alipay_trade_page_pay(
            out_trade_no=order_id,
            total_amount=str(total_pay),
            subject='天天生鲜%s' % order_id,
            return_url=None,
            notify_url=None  # 可选, 不填则使用默认notify url
        )
        # 动态设置响应的支付url
        pay_url = 'https://openapi.alipaydev.com/gateway.do?' + order_string
        setattr(self, 'response', pay_url)

    @property
    def data(self):
        # 获取响应的url
        response = getattr(self, 'response', None)
        # 返回应答
        return ReturnDict({'pay_url': response, 'msg': '请求成功!'}, serializer=self)


class CheckOrderSerializer(AbstractPaySerializer):

    # 采用前端轮询的方式来查询是否支付
    def save(self, **kwargs):
        order = self.validated_data
        response = self.alipay.api_alipay_trade_query(order.order_id)
        code = response.get('code')
        if code == '10000' and response.get('trade_status') == 'TRADE_SUCCESS':
            train_no = response.get('trade_no')
            order.trade_no = train_no
            # 将支付状态改为待评价
            order.order_status = 4
            order.save()
            setattr(self, 'response', {'msg': '支付成功!', 'code': code})
        elif (code == '10000' and response.get('trade_status') == 'WAIT_BUYER_PAY') or code == '40004':
            # 等待支付
            setattr(self, 'response', {'msg': '等待支付!', 'code': code})
        else:
            setattr(self, 'response', {'msg': '支付失败!', 'code': code})

    @property
    def data(self):
        response = getattr(self, 'response', None)
        return ReturnDict(response, serializer=self)


# 评论的序列化器
class CommentModelSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='order.user.username', read_only=True)

    class Meta:
        model = models.OrderGoods
        fields = ['comment', 'user', 'insert_time', 'update_time', 'id']
        extra_kwargs = {
            'insert_time': {'format': '%Y-%m-%d %H:%M:%S', 'read_only': True},
            'update_time': {'format': '%Y-%m-%d %H:%M:%S', 'read_only': True},
            'id': {'read_only': True},
        }

        # 评论中可能有为空字符的,前端可以设置为`该用户未发表任何评论`或者后端保存的时候默认存储


# 查看评论
class CommentReadModelSerializer(serializers.ModelSerializer):
    results = serializers.ManyRelatedField(child_relation=CommentModelSerializer(), source='ordergoods_set')

    class Meta:
        model = GoodsSKU
        fields = ['results']


class UpdateCommentModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.OrderGoods
        fields = ['comment']
