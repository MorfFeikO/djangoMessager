from registration.models import User
from rest_framework import viewsets, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Message, Profile
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


class FollowUnfollowView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk, req_type, format=None):
        current_profile = Profile.current_profile(request.user)
        other_profile = Profile.other_profile(pk)

        if req_type == 'follow':
            # Add selected user to `follows` and to selected user's `followers`
            current_profile.follows.add(other_profile)
            other_profile.followers.add(current_profile)

            # update messages with selected user `messages`
            other_user_messages = other_profile.user.messages.all()
            for message in other_user_messages:
                current_profile.user.messages.add(message)

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
