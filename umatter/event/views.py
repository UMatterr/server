import logging
import traceback as tb

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from user.utils import auth_user, control_request_method

from .forms import EventForm
from .models import Event, EventType
from .serializers import EventSerializer, EventTypeSerializer
from django.http import HttpResponseBadRequest


logger = logging.getLogger(__name__)

@csrf_exempt
@auth_user
@control_request_method(method=('GET', 'POST'))
def get_or_post_event(request):

    kakao_id = request.kakao_id
    access_token = request.COOKIES.get('access_token')
    refresh_token = request.COOKIES.get('refresh_token')
    logger.info(
        f"user kakao id: {kakao_id}, {access_token}, {refresh_token}"
    )
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
            status=400
        )
    except Event.MultipleObjectsReturned:
        return HttpResponseBadRequest(
            content={'Multiple events'},
            status=400
        )
    except:
        logger.error(tb.format_exc())
        return HttpResponseBadRequest(
            content={'Unknown error'},
            status=400
        )
    return HttpResponse(content={'Success'}, status=200)
