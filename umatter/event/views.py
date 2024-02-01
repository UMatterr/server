import json
import logging
import traceback as tb

from django.http import (
    HttpResponse, HttpResponseBadRequest,
    JsonResponse,
)
from django.views.decorators.csrf import csrf_exempt

from friend.models import Friend
from user.utils import auth_user, control_request_method

from .forms import EventForm
from .models import CustomEventType, Event, EventType
from .serializers import (
    EventSerializer, EventTypeSerializer,
)


logger = logging.getLogger(__name__)

@csrf_exempt
@auth_user
@control_request_method(method=('GET', 'POST'))
def get_or_post_event(request):

    user = request.user
    if request.method == 'POST':
        logger.info(request.POST)
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse(content={'Saved'}, status=200)
        return HttpResponse(content={'Not valid'}, status=400)

    if request.method == 'GET':
        event = Event.objects.all()
        data = EventSerializer(event, many=True).data
        logger.info(f"event: {event}")
        logger.info(f"event serialized: {data}")
        return HttpResponse(content=data, status=200)


@csrf_exempt
@auth_user
@control_request_method(method=('DELETE'))
def delete_event(request, uuid):
    try:
        event = Event.objects.get(id=uuid)
        logger.info(f"event: {event}")
        event.delete()

    except Event.DoesNotExist:
        return HttpResponseBadRequest(
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
    data = json.loads(request.body)
    logger.info("data: %s", data)
    if data is None:
        return HttpResponseBadRequest(
            content={'No data'},
            status=400
        )

    try:
        name = data['name']
        friend = Friend.objects.get(
            id=data['friendId']
        )
        event_type = EventType.objects.get(
            id=int(data['eventTypeId'])
        )
        custom_event_type = None
        date = data['date']
        repeat = data['repeat']

    except EventType.DoesNotExist:
        return HttpResponseBadRequest(
            content={'No event type'},
            status=400
        )

    except:
        logger.error(tb.format_exc())
        return HttpResponseBadRequest(
            content={'Unknown error'},
            status=400
        )

    if event_type.name == '기타':
        logger.info("name: %s, %s", name, event_type.name)
        if name is None:
            return HttpResponseBadRequest(
                content={'No event name'},
            )

        try:
            custom_event_type = CustomEventType.objects.get(name=name)
            logger.info(
                "Retrieved an existing custom event type: %s",
                custom_event_type
            )

        except CustomEventType.DoesNotExist:
            custom_event_type = CustomEventType(name=name)
            custom_event_type.save()
            logger.info(
                "Created a new custom event type: %s",
                custom_event_type
            )
        name = custom_event_type.name

    else:
        name = event_type.name

    try:
        event = Event(
            name=name,
            friend=friend,
            event_type=event_type,
            custom_event_type=custom_event_type,
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
