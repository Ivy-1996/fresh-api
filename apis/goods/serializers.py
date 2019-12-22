from rest_framework import serializers
from . import models


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
    class Meta:
        model = models.GoodsSKU
        # fields = '__all__'
        exclude = ['insert_time', 'update_time', 'is_delete']
        # depth = 1


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
