from rest_framework import serializers

from registration.models import User

from .models import Message, Profile


class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Profile
        fields = ['url', 'follows', 'followers']


class UserSerializer(serializers.HyperlinkedModelSerializer):
    profile = ProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = ['url', 'email', 'username', 'messages', 'profile', 'liked']
        read_only_fields = ['email', 'messages']


class MessageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Message
        fields = ['url', 'owner', 'body', 'created_at', 'liked_by']
        read_only_fields = ['owner', 'liked_by']
