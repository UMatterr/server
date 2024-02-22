import json
import logging
import traceback as tb

from django.http import (
    HttpResponse, HttpResponseBadRequest,
    HttpResponseNotFound, JsonResponse,
)
from django.views.decorators.csrf import csrf_exempt

from friend.models import Friend
from user.utils import auth_user, control_request_method

from .models import Event, EventType
from .serializers import (
    EventListSerializer, EventTypeSerializer,
    FriendEventListSerializer,
)


logger = logging.getLogger(__name__)

@csrf_exempt
@auth_user
@control_request_method()
def get_events(request):

    user = request.user
    if request.method == 'GET':
        friend_name = request.GET.get("name", "")
        event_type = request.GET.get("etype", "")

        event = Event.objects.filter(
            user__id=user.id
        )
        logger.info("before filtering: %s", event)

        if friend_name != "" and event_type != "":
            event = event.filter(
                event_type__id=event_type,
                friend__name=friend_name
            )

        elif friend_name != "":
            event = event.filter(
                friend__name=friend_name
            )

        elif event_type != "":
            event = event.filter(
                event_type__id=event_type,
            )

        logger.info("before filtering: %s", event)

        data = EventListSerializer(event, many=True).data
        logger.info("event serialized: %s", data)

        return JsonResponse(data=data, status=200, safe=False)


@csrf_exempt
@auth_user
@control_request_method()
def get_event_by_friend(request, pk):

    user = request.user
    if request.method == 'GET':
        event = Event.objects.filter(user__id=user.id, friend_id=pk)
        logger.info(f"event: {event}")
        data = FriendEventListSerializer(event, many=True).data
        logger.info(f"event serialized: {data}")
        return JsonResponse(data=data, status=200, safe=False)


@csrf_exempt
@auth_user
@control_request_method(method=('DELETE'))
def delete_event(request, pk):
    try:
        event = Event.objects.get(id=pk)
        logger.info(f"event: {event}")
        event.delete()

    except Event.DoesNotExist:
        return HttpResponseNotFound(
            content={'No event'},
        )

    except Event.MultipleObjectsReturned:
        return HttpResponseBadRequest(
            content={'Multiple events'},
        )

    except:
        logger.error(tb.format_exc())
        return HttpResponseBadRequest(
            content={'Unknown error'},
        )

    return HttpResponse(content={'Success'}, status=204)


@csrf_exempt
@auth_user
@control_request_method()
def get_event_type(request):
    try:
        event_type = EventType.objects.all()
        data = EventTypeSerializer(event_type, many=True).data
        logger.info(f"event: {data}")

    except:
        logger.error(tb.format_exc())
        return HttpResponseBadRequest(
            content={'Unknown error'},
            status=400
        )

    return JsonResponse(
        data=data,
        status=200,
        safe=False,
    )


@csrf_exempt
@auth_user
@control_request_method(method=('POST'))
def create_event(request):
    user = request.user
    data = json.loads(request.body)
    logger.info("data: %s", data)
    if data is None:
        return HttpResponseBadRequest(
            content={'No data'},
            status=400
        )

    try:
        # name = data['name']
        friend = Friend.objects.get(
            id=data['friendId']
        )
        event_type = EventType.objects.get(
            id=int(data['eventTypeId'])
        )
        name = event_type.name
        date = data['date']
        repeat = data['repeat']

    except Friend.DoesNotExist:
        return HttpResponseNotFound(
            content={'No event type'},
        )

    except EventType.DoesNotExist:
        return HttpResponseNotFound(
            content={'No event type'},
        )

    except:
        logger.error(tb.format_exc())
        return HttpResponseBadRequest(
            content={'Unknown error'},
            status=400
        )

    try:
        event = Event(
            name=name,
            user=user,
            friend=friend,
            event_type=event_type,
            date=date,
            repeat=repeat,
        )
        event.save()
        logger.info(
            "Created a new event: %s",
            event
        )

    except:
        logger.error(tb.format_exc())
        return HttpResponseBadRequest(
            content={'Unknown error'},
            status=400
        )

    return JsonResponse(
        data={"eventId": event.id},
        status=201,
        safe=False,
    )
