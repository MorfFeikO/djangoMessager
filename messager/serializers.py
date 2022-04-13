from registration.models import User
from rest_framework import serializers
from .models import Message, Profile


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'email', 'username', 'messages']


class MessageSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Message
        fields = ['url', 'owner', 'body', 'created_at']


class FollowSerializer(serializers.ModelSerializer):
    follows = UserSerializer(many=True, read_only=True)
    followers = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Profile
        fields = ['follows', 'followers']
        read_only_fields = ['follows', 'followers']
