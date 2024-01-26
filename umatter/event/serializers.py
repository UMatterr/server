from rest_framework import serializers

from friend.serializers import FriendSerializer
from .models import Event, EventType


class EventTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = EventType
        fields = '__all__'


class EventSerializer(serializers.ModelSerializer):

    event_type = EventTypeSerializer(many=True, read_only=True)
    friend = FriendSerializer(many=True, read_only=True)

    class Meta:
        model = Event
        fields = '__all__'
