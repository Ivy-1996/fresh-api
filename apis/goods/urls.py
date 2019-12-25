from rest_framework import routers

from . import views

route = routers.DefaultRouter(trailing_slash=False)

route.register('type', views.GoodsTypeApi, basename='type')
route.register('banner', views.GoodsBannerApi, basename='banner')
route.register('sku', views.GoodsSkuApi, basename='sku')  # 原生查询
route.register('haystack-sku', views.GoodsSkuHaystackViewApi, basename='haystack-sku')  # 搜索引擎查询
route.register('image', views.GoodsImageApi, basename='image')
route.register('index/banner', views.IndexTypeGoodsBannerApi, basename='index-banner')
route.register('promotion/banner', views.IndexPromotionBannerApi, basename='promotion-banner')
route.register('', views.GoodsApi, basename='index')
urlpatterns = route.urls
