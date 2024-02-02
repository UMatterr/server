from rest_framework import serializers

from event.models import Event

from .models import Friend


class FriendSerializer(serializers.ModelSerializer):

    friendId = serializers.SerializerMethodField('get_alternative_id')
    count = serializers.SerializerMethodField('get_event_count')

    class Meta:
        model = Friend
        fields = ['friendId', 'name', 'count']

    def get_alternative_id(self, obj):
        return obj.id

    def get_event_count(self, obj):
        return Event.objects.filter(
            user__id=self.context.get("user_id"),
            friend__id=obj.id,
        ).count()


class FriendDetailSerializer(serializers.ModelSerializer):

    friendName = serializers.SerializerMethodField('get_alternative_name')

    class Meta:
        model = Friend
        fields = ['friendName']

    def get_alternative_name(self, obj):
        return obj.name
