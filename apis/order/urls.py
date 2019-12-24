from rest_framework import routers

from . import views

route = routers.DefaultRouter(trailing_slash=False)
route.register('pay', views.PayOrderApi, basename='pay')
route.register('check', views.PayOrderCheckApi, basename='check')
route.register('comment', views.CommentApi, basename='comment')
route.register('', views.OrderApi, basename='order')

urlpatterns = route.urls
