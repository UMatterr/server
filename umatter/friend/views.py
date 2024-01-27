import logging

from rest_framework.views import APIView
from rest_framework.response import Response

from event.models import Event, EventType, Friend
from event.serializers import EventSerializer, EventTypeSerializer
from user.utils import auth_user
from .models import Friend
from .serializers import FriendSerializer


logger = logging.getLogger(__name__)

class FriendListView(APIView):
    def get(self, request):
        friends = Friend.objects.all()
        serializer = FriendSerializer(friends, many=True)
        return Response(serializer.data)

    def create(self, request):
        pass


class FriendView(APIView):
    def get(self, request):
        friend = Friend.objects.get(id=request.id)
        serializer = FriendSerializer(friend, many=True)
        return Response(serializer.data)
