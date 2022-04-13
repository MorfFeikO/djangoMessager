from django.shortcuts import get_object_or_404

from rest_framework import viewsets, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action

from registration.models import User

from .models import Message, Profile
from .serializers import UserSerializer, MessageSerializer, FollowSerializer
from .permissions import IsOwnerOrReadOnly


class UserViewSet(viewsets.ModelViewSet):
    """API endpoint that allows users to be viewed or editied."""
    queryset = User.objects.all().order_by('-created_at')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    @action(
        methods=['post'],
        detail=True,
        permission_classes=[permissions.IsAuthenticated, IsOwnerOrReadOnly],
        serializer_class=FollowSerializer,
    )
    def follow(self, request, pk, format=None):
        active_user = get_object_or_404(Profile, user=request.user)
        other_user = get_object_or_404(Profile, pk=pk)
        if active_user.is_follow(other_user):
            return Response(
                {"follow": "User is already followed."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        active_user.follows.add(other_user)
        other_user.followers.add(active_user)
        return Response(
            {"follow": "Successfully follows other user"},
            status=status.HTTP_200_OK,
        )

    @action(
        methods=['post'],
        detail=True,
        permission_classes=[permissions.IsAuthenticated, IsOwnerOrReadOnly],
        serializer_class=FollowSerializer,
    )
    def unfollow(self, request, pk, format=None):
        active_user = get_object_or_404(Profile, user=request.user)
        other_user = get_object_or_404(Profile, pk=pk)
        if not active_user.is_follow(other_user):
            return Response(
                {"unfollow": "User is already unfollowed."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        active_user.follows.remove(other_user)
        other_user.followers.remove(active_user)
        return Response(
            {"unfollow": "Successfully unfollow other user"},
            status=status.HTTP_200_OK,
        )


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all().order_by('-created_at')
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# work on serializer followers
