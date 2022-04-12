from django.urls import path

from .views import RegistrationAPIView


app_name = 'registration'

urlpatterns = [
    path('', RegistrationAPIView.as_view(), name='registration'),
    ]
