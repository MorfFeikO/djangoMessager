from django.urls import path, include
from rest_framework import routers
from . import views


message_router = routers.DefaultRouter()
message_router.register(r'users', views.UserViewSet)
message_router.register(r'messages', views.MessageViewSet)
message_router.register(r'profiles', views.ProfileViewSet)

urlpatterns = [
    path('', include(message_router.urls)),
]
