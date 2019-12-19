from django.core.validators import BaseValidator

from rest_framework.serializers import ValidationError
from . import ext


class PhonenumValidator(BaseValidator):
    message = '手机号码格式不正确'

    def clean(self, x: str):
        return x.strip()

    def compare(self, a, b):
        return not ext.is_legal_phone(a)


# 序列化器的手机号码验证使用
def phonenum_validator(value):
    if not ext.is_legal_phone(value):
        raise ValidationError({'phonenum': ['手机号码格式不正确']})
