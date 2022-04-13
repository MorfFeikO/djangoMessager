from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from registration.models import User

from .models import Message, Profile
from .serializers import UserSerializer, MessageSerializer
from .permissions import IsOwnerOrReadOnly


class UserViewSet(viewsets.ModelViewSet):
    """API endpoint that allows users to be viewed or editied."""
    queryset = User.objects.all().order_by('-created_at')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all().order_by('-created_at')
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class FollowUnfollowView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk, req_type, format=None):
        current_profile = get_object_or_404(Profile, user=request.user)
        other_profile = get_object_or_404(Profile, pk=pk)

        if req_type == 'follow':
            current_profile.follows.add(other_profile)
            other_profile.followers.add(current_profile)

            return Response(
                {"follow": "Successfully follows other user"},
                status=status.HTTP_200_OK,
            )
        elif req_type == 'unfollow':
            current_profile.follows.remove(other_profile)
            other_profile.followers.remove(current_profile)
            return Response(
                {"unfollow": "Successfully unfollow other user"},
                status=status.HTTP_200_OK,
            )


# check if user is already in the list, or is yet not
