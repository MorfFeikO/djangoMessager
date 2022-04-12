from registration.models import User
from rest_framework import viewsets, permissions

from .models import Message
from .serializers import UserSerializer, MessageSerializer


class UserViewSet(viewsets.ModelViewSet):
    """API endpoint that allows users to be viewed or editied."""
    queryset = User.objects.all().order_by('-created_at')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all().order_by('-created_at')
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
