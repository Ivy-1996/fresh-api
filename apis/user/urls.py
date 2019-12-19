from rest_framework import routers
from . import views

route = routers.DefaultRouter(trailing_slash=False)

route.register('register', views.RegisterApi, basename='user')
route.register('login', views.LoginApi, basename='user')
urlpatterns = route.urls
