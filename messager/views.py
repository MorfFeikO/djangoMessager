from django.shortcuts import get_object_or_404

from rest_framework import viewsets, permissions, mixins
from rest_framework.decorators import action

from registration.models import User

from .models import Message, Profile
from .serializers import (
    UserSerializer,
    MessageSerializer,
    ProfileSerializer,
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
        detail=True,
        permission_classes=[permissions.IsAuthenticated, IsOwnerOrReadOnly],
    )
    def follow(self, request, pk, task="follow"):
        active_profile = get_object_or_404(Profile, user=request.user)
        other_profile = get_object_or_404(Profile, pk=pk)
        if active_profile.is_follow(other_profile.user):
            return repeated_action_response(task)
        active_profile.follows.add(other_profile.user)
        other_profile.followers.add(active_profile.user)
        return success_response(task)

    @action(
        detail=True,
        permission_classes=[permissions.IsAuthenticated, IsOwnerOrReadOnly],
    )
    def unfollow(self, request, pk, task="unfollow"):
        active_profile = get_object_or_404(Profile, user=request.user)
        other_profile = get_object_or_404(Profile, pk=pk)
        if not active_profile.is_follow(other_profile.user):
            return repeated_action_response(task)
        active_profile.follows.remove(other_profile.user)
        other_profile.followers.remove(active_profile.user)
        return success_response(task)


class ProfileViewSet(mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin,
                     mixins.ListModelMixin,
                     viewsets.GenericViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all().order_by('-created_at')
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    @action(
        detail=True,
        permission_classes=[permissions.IsAuthenticated, IsOwnerOrReadOnly],
    )
    def like(self, request, pk, task="like"):
        message = get_object_or_404(Message, pk=pk)
        if message.is_liked_by(request.user):
            return repeated_action_response(task)
        message.liked_by.add(request.user)
        return success_response(task)

    @action(
        detail=True,
        permission_classes=[permissions.IsAuthenticated, IsOwnerOrReadOnly],
    )
    def dislike(self, request, pk, task="dislike"):
        message = get_object_or_404(Message, pk=pk)
        if not message.is_liked_by(request.user):
            return repeated_action_response(task)
        message.liked_by.remove(request.user)
        return success_response(task)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

# make postgres comm
# merge `task/add-jwt`
