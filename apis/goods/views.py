from utils.views import ReadOnlyModelViewSet
from . import models
from . import serializers


class GoodsApi(ReadOnlyModelViewSet):
    queryset = models.Goods.objects.all()
    serializer_class = serializers.GoodsModelSerializer


class GoodsTypeApi(ReadOnlyModelViewSet):
    queryset = models.GoodsType.objects.all()
    serializer_class = serializers.GoodsTypeModelSerializer


class GoodsBannerApi(ReadOnlyModelViewSet):
    queryset = models.IndexGoodsBanner.objects.all()
    serializer_class = serializers.GoodsBannerModelSerializer


class GoodsSkuApi(ReadOnlyModelViewSet):
    queryset = models.GoodsSKU.objects.all()
    serializer_class = serializers.GoodsSkuModelSerializer


class GoodsImageApi(ReadOnlyModelViewSet):
    queryset = models.GoodsImage.objects.all()
    serializer_class = serializers.GoodsImageModelSerializer


class IndexTypeGoodsBannerApi(ReadOnlyModelViewSet):
    queryset = models.IndexTypeGoodsBanner.objects.all()
    serializer_class = serializers.IndexTypeGoodsBannerModelSerializer


class IndexPromotionBannerApi(ReadOnlyModelViewSet):
    queryset = models.IndexPromotionBanner.objects.all()
    serializer_class = serializers.IndexPromotionBannerModelSerializer
