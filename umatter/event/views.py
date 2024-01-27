import logging

from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Event, EventType
from .serializers import EventSerializer, EventTypeSerializer


logger = logging.getLogger(__name__)

class EventListView(APIView):
    def get(self, request):
        events = Event.objects.all()
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)


class EventDetailView(APIView):
    def get(self, request):
        event = Event.objects.get(id=request.id)
        serializer = EventSerializer(event, many=True)
        return Response(serializer.data)


class EventTypeListView(APIView):
    def get(self, request):
        event_types = EventType.objects.all()
        serializer = EventTypeSerializer(event_types, many=True)
        return Response(serializer.data)


class EventTypeDetailView(APIView):
    def get(self, request):
        event_type = EventType.objects.get(id=request.id)
        serializer = EventTypeSerializer(event_type, many=True)
        return Response(serializer.data)
