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


class EventListSerializer(serializers.ModelSerializer):

    eventId = serializers.SerializerMethodField('get_alternative_id')
    eventName = serializers.SerializerMethodField('get_alternative_event_name')
    eventType = serializers.SerializerMethodField('get_alternative_event_type_id')
    friendName = serializers.SerializerMethodField('get_alternative_friend_name')

    class Meta:
        model = Event
        fields = [
            'eventId', 'eventName', 'eventType', 'friendName', 'date', 'repeat',
        ]

    def get_alternative_id(self, obj):
        return obj.id

    def get_alternative_event_name(self, obj):
        return obj.name

    def get_alternative_event_type_id(self, obj):
        return obj.event_type.id

    def get_alternative_friend_name(self, obj):
        return obj.friend.name


class FriendEventListSerializer(serializers.ModelSerializer):

    eventId = serializers.SerializerMethodField('get_alternative_id')
    eventName = serializers.SerializerMethodField('get_alternative_event_name')

    class Meta:
        model = Event
        fields = [
            'eventId', 'eventName',
        ]

    def get_alternative_id(self, obj):
        return obj.id

    def get_alternative_event_name(self, obj):
        return obj.name
