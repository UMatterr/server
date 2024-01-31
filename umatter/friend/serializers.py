from rest_framework import serializers

from user.serializers import UserSerializer

from .models import Friend


class FriendSerializer(serializers.ModelSerializer):

    # user = UserSerializer(read_only=True)

    class Meta:
        model = Friend
        fields = ['id', 'name']
