from rest_framework import serializers

from friend.serializers import FriendSerializer
from .models import Event, EventType


class EventTypeSerializer(serializers.ModelSerializer):

    eventTypeId = serializers.SerializerMethodField('get_alternative_name')

    class Meta:
        model = EventType
        fields = ['eventTypeId', 'name']

    def get_alternative_name(self, obj):
        return obj.id


class EventSerializer(serializers.ModelSerializer):

    event_type = EventTypeSerializer(many=True, read_only=True)
    friend = FriendSerializer(many=True, read_only=True)

    class Meta:
        model = Event
        fields = '__all__'
