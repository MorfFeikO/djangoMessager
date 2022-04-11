from django.contrib.auth.models import User
from rest_framework import viewsets, permissions

from .serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    """API endpoint that allows users to be viewed or editied."""
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
