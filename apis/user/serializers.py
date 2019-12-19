from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login, logout

from rest_framework import serializers
from rest_framework.utils.serializer_helpers import ReturnDict

from itsdangerous import JSONWebSignatureSerializer

import uuid

# 注册模块
from tasks.task import send_register_mail


class RegisterSerializer(serializers.Serializer):
    allow = serializers.CharField(max_length=5)
    r_password = serializers.CharField(max_length=20)
    username = serializers.CharField(max_length=8, min_length=5)
    password = serializers.CharField(max_length=16, min_length=6)
    email = serializers.EmailField(max_length=20)

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

    def create(self, validated_data):
        user = authenticate(**validated_data)
        if user:
            request = self.context.get('request')
            login(request, user)
            return validated_data
        raise serializers.ValidationError({'password': ['用户名或密码错误!']})

    @property
    def data(self):
        return ReturnDict({'msg': '登录成功!'}, serializer=self)
