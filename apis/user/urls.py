from rest_framework import routers
from . import views

route = routers.DefaultRouter(trailing_slash=False)

route.register('register', views.RegisterApi, basename='register')
route.register('login', views.LoginApi, basename='login')
route.register('active', views.UserActiveApi, basename='active')
route.register('logout', views.LougoutApi, basename='logout')
route.register('address', views.AddressApi, basename='address')
urlpatterns = route.urls
