from django.db import models
from . import validators


class BaseModel(models.Model):
    insert_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    is_delete = models.BooleanField(default=False)


class PhonenumField(models.CharField):
    def __init__(self, *args, **kwargs):
        super(PhonenumField, self).__init__(*args, *kwargs)
        self.max_length = 11
        self.validators.append(validators.PhonenumValidator(self.max_length))
