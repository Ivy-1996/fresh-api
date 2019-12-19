import django_filters
from django_filters.utils import get_all_model_fields

ALL_FIELDS = '__all__'


class FilterSet(django_filters.FilterSet):

    def __new__(cls, *args, **kwargs):
        cls.Meta = getattr(cls, 'Meta')
        fields = cls.init_lookup_expr(cls.Meta)
        setattr(cls.Meta, 'fields', fields)
        return super().__new__(cls)

    @classmethod
    def init_lookup_expr(cls, meta):
        fields = getattr(meta, 'fields')
        if fields == ALL_FIELDS:
            lookup_expr = getattr(meta, 'lookup_expr', None)
            if lookup_expr is not None:
                result = cls.start_trans_fields(meta, lookup_expr)
                return result

    @classmethod
    def start_trans_fields(cls, meta, lookup_expr):
        fields = cls.get_trans_fields(meta)
        result = dict()
        for field in fields:
            result[field] = lookup_expr
        return result

        # print('new', self._meta.fields)

    @classmethod
    def get_trans_fields(cls, meta):
        model = getattr(meta, 'model')
        fields = get_all_model_fields(model)
        return fields
