from rest_framework import routers
from . import views

route = routers.DefaultRouter(trailing_slash=False)

route.register('add', views.AddCartApi, basename='add')
route.register('info', views.CartInfoApi, basename='info')
route.register('update', views.UpdateCartApi, basename='update')
route.register('delete', views.DeleteCartApi, basename='deletedelete')

urlpatterns = route.urls
