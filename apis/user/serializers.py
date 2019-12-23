from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import PermissionDenied

from rest_framework import serializers
from rest_framework.utils.serializer_helpers import ReturnDict

from itsdangerous import JSONWebSignatureSerializer, BadSignature

import uuid

from tasks.task import send_register_mail
from utils.validators import phonenum_validator

from goods.models import GoodsSKU
from . import models

CREATE = 'create'


# 注册模块
class RegisterSerializer(serializers.ModelSerializer):
    allow = serializers.CharField(max_length=5)
    r_password = serializers.CharField(max_length=20)
    username = serializers.CharField(max_length=8, min_length=5)
    password = serializers.CharField(max_length=16, min_length=6)
    email = serializers.EmailField(max_length=20)

    class Meta:
        model = get_user_model()
        fields = ['allow', 'r_password', 'username', 'password', 'email']

    # 验证是否同意协议
    def validate_allow(self, attr):
        if attr != 'on':
            raise serializers.ValidationError({'allow': ['请同意协议']})
        return attr

    # 验证用户名是否存在
    def validate_username(self, attr):
        if self.is_exist({'username': attr}):
            raise serializers.ValidationError({'username': ['用户名已存在']})
        return attr

    # 验证邮箱是否存在
    def validate_email(self, attr):
        if self.is_exist({'email': attr}):
            raise serializers.ValidationError({'username': ['邮箱已被注册']})
        return attr

    @staticmethod
    def is_exist(item: dict):
        model = get_user_model()
        try:
            model.objects.get(**item)
        except model.DoesNotExist:
            return False
        return True

    # 验证密码的一致性
    def validate(self, attrs):
        password = attrs.get('password')
        r_password = attrs.get('r_password')
        if password != r_password:
            raise serializers.ValidationError({'r_password': '两次密码输入不一致'})
        attrs.pop('allow')
        attrs.pop('r_password')
        return attrs

    def save(self, **kwargs):
        model = get_user_model()
        user = model.objects.create_user(is_active=False, **self.validated_data)
        serializer = JSONWebSignatureSerializer(settings.SECRET_KEY)
        data = {'user': user.id, 'uuid': uuid.uuid4().hex}
        token = serializer.dumps(data).decode()
        email = self.validated_data.get('email')
        username = self.validated_data.get('username')
        send_register_mail(email, username, token)

    @property
    def data(self):
        resp = {'msg': '注册成功!'}
        return ReturnDict(resp, serializer=self)


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=8, min_length=5)
    password = serializers.CharField(max_length=16, min_length=6)

    def save(self, **kwargs):
        user = authenticate(**self.validated_data)
        if user:
            if user.is_active is False:
                raise serializers.ValidationError({'username': ['用户未激活!']})
            request = self.context.get('request')
            login(request, user)
        else:
            raise serializers.ValidationError({'password': ['用户名或密码错误!']})

    @property
    def data(self):
        return ReturnDict({'msg': '登录成功!'}, serializer=self)


class UserActiveSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=255)

    # 解密token
    def validate(self, attrs):
        token = attrs.get('token')
        serializer = JSONWebSignatureSerializer(settings.SECRET_KEY)
        try:
            data = serializer.loads(token)
        except BadSignature:
            raise PermissionDenied
        return data


class AddressModelSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = models.Address
        exclude = ['is_delete']
        extra_kwargs = {
            'insert_time': {'read_only': True},
            'update_time': {'read_only': True},
            'phone': {'validators': [phonenum_validator]}
        }

    # 将以前的所有的默认地址改为False(其实也只有一个)
    # 再转给父类的create执行操作
    def create(self, validated_data):
        is_default = validated_data.get('is_default')
        if is_default is True:
            self.Meta.model.objects.filter(is_default=True, is_delete=False).update(is_default=False)
        return super(AddressModelSerializer, self).create(validated_data)

    # 同上
    def update(self, instance, validated_data):
        self.Meta.model.objects.filter(is_default=True, is_delete=False).update(is_default=False)
        return super().update(instance, validated_data)


class HistorySerializer(serializers.Serializer):
    histories = serializers.ListField(child=serializers.IntegerField())

    # 不要使用`PrimaryKeyRelatedField`, 它的内部是通过`objects.get`的方式获取的,序列化多个需要合并queryset
    # histories = serializers.ListField(child=serializers.PrimaryKeyRelatedField(queryset=GoodsSKU.objects.all()))

    # 获取合并`queryset`对象
    def validate(self, attrs):
        histories = attrs.get('histories')
        # 设置一个空的`queryset`
        instance = GoodsSKU.objects.none()
        # 合并浏览记录列表的`queryset`
        for history in histories:
            good = GoodsSKU.objects.filter(pk=history)
            instance = instance | good
        return instance
