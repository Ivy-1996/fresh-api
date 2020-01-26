from rest_framework import serializers

from drf_haystack.serializers import HaystackSerializer

from order.serializers import CommentModelSerializer

from . import models
from . import search_indexes


class GoodsModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Goods
        fields = '__all__'


class GoodsTypeModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.GoodsType
        fields = '__all__'


class GoodsBannerModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.IndexGoodsBanner
        fields = '__all__'


class GoodsSkuModelSerializer(serializers.ModelSerializer):
    # comment = serializers.ManyRelatedField(source='ordergoods_set', child_relation=CommentModelSerializer(),
    #                                        read_only=True, required=False)

    class Meta:
        model = models.GoodsSKU
        exclude = ['create_time', 'update_time', 'delflag', ]
        depth = 1


class GoodsSkuHaystackSerializer(HaystackSerializer):
    object = GoodsSkuModelSerializer(read_only=True)

    class Meta:
        index_classes = [search_indexes.GoodsSKUIndex]
        fields = ['object', 'name', 'desc', 'detail']
        ignore_fields = ["autocomplete"]

        # The `field_aliases` attribute can be used in order to alias a
        # query parameter to a field attribute. In this case a query like
        # /search/?q=oslo would alias the `q` parameter to the `autocomplete`
        # field on the index.
        field_aliases = {
            "q": "autocomplete"
        }


class GoodsImageModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.GoodsImage
        fields = '__all__'
        depth = 1


class IndexTypeGoodsBannerModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.IndexTypeGoodsBanner
        fields = '__all__'
        depth = 1


class IndexPromotionBannerModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.IndexPromotionBanner
        fields = '__all__'
