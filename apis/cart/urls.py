from rest_framework import routers
from . import views

route = routers.DefaultRouter(trailing_slash=False)

route.register('add', views.AddCartApi, basename='add')
route.register('info', views.CartInfoApi, basename='info')

urlpatterns = route.urls
