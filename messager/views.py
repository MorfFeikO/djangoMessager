from django.shortcuts import get_object_or_404

from rest_framework import viewsets, permissions, mixins, generics
from rest_framework.decorators import action

from registration.models import User

from .models import Message, Profile
from .serializers import (
    UserSerializer,
    MessageSerializer,
    FollowSerializer,
    LikeSerializer,
)
from .permissions import IsOwnerOrReadOnly
from .utils import success_response, repeated_action_response


class UserViewSet(mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  mixins.ListModelMixin,
                  viewsets.GenericViewSet):
    """API endpoint that allows users to be viewed or edited."""
    queryset = User.objects.all().order_by('-created_at')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    @action(
        methods=['post', 'get'],
        detail=True,
        permission_classes=[permissions.IsAuthenticated, IsOwnerOrReadOnly],
        serializer_class=FollowSerializer,
    )
    def follow(self, request, pk, task="follow", format=None):
        active_user = get_object_or_404(Profile, user=request.user)
        other_user = get_object_or_404(Profile, pk=pk)
        if active_user.is_follow(other_user):
            return repeated_action_response(task)
        active_user.follows.add(other_user)
        other_user.followers.add(active_user)
        return success_response(task)

    @action(
        methods=['post', 'get'],
        detail=True,
        permission_classes=[permissions.IsAuthenticated, IsOwnerOrReadOnly],
        serializer_class=FollowSerializer,
    )
    def unfollow(self, request, pk, task="unfollow", format=None):
        active_user = get_object_or_404(Profile, user=request.user)
        other_user = get_object_or_404(Profile, pk=pk)
        if not active_user.is_follow(other_user):
            return repeated_action_response(task)
        active_user.follows.remove(other_user)
        other_user.followers.remove(active_user)
        return success_response(task)


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all().order_by('-created_at')
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    @action(
        methods=['post'],
        detail=True,
        permission_classes=[permissions.IsAuthenticated, IsOwnerOrReadOnly],
        serializer_class=LikeSerializer,
    )
    def like(self, request, pk, task="like", format=None):
        active_user = get_object_or_404(Profile, user=request.user)
        message = get_object_or_404(Message, pk=pk)
        if message.is_liked_by(active_user):
            return repeated_action_response(task)
        message.liked_by.add(active_user)
        return success_response(task)

    @action(
        methods=['post'],
        detail=True,
        permission_classes=[permissions.IsAuthenticated, IsOwnerOrReadOnly],
        serializer_class=LikeSerializer,
    )
    def dislike(self, request, pk, task="dislike", format=None):
        active_user = get_object_or_404(Profile, user=request.user)
        message = get_object_or_404(Message, pk=pk)
        if not message.is_liked_by(active_user):
            return repeated_action_response(task)
        message.liked_by.remove(active_user)
        return success_response(task)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

# work on get followers and likes
# run tests and find out what should we write to test (make comm.)
# add pre-commit and pre-push and make run this separately
# .env
# merge `task/add-jwt`
# django-email-confirmation
# django-any (for tests)
