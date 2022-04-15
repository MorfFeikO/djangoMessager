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
        fields = ['url', 'email', 'username', 'messages', 'profile']
        read_only_fields = ['email', 'messages']


class MessageSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Message
        fields = ['url', 'owner', 'body', 'created_at']


class LikeSerializer(serializers.ModelSerializer):
    like = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Profile
        fields = ['like']
        read_only_fields = ['like']
