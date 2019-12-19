from rest_framework import serializers
from .validators import phonenum_validator


class PhonenumField(serializers.CharField):
    def __init__(self, **kwargs):
        super(PhonenumField, self).__init__(**kwargs)
        self.validators.append(phonenum_validator)
