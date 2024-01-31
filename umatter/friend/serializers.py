from rest_framework import serializers

from .models import Friend


class FriendSerializer(serializers.ModelSerializer):

    friendId = serializers.SerializerMethodField('get_alternative_name')

    class Meta:
        model = Friend
        fields = ['friendId', 'name']

    def get_alternative_name(self, obj):
        return obj.id
