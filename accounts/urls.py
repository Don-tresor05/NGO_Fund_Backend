from django.urls import path, include
from rest_framework import routers
from accounts.views import UserViewset, LoginMixin

route = routers.DefaultRouter()
route.register('user', UserViewset)
route.register('login',LoginMixin,basename="login")



urlpatterns = [
    path('', include(route.urls)),
]

