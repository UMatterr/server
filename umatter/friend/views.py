import json
import logging
import traceback as tb

from django.http import (
    HttpResponse, HttpResponseBadRequest,
    HttpResponseNotFound, JsonResponse,
)
from django.views.decorators.csrf import csrf_exempt

from rest_framework import status
from rest_framework.response import Response

from user.utils import auth_user, control_request_method

from .models import Friend
from .serializers import (
    FriendDetailSerializer,
    FriendSerializer,
)
from .services import count_events_for_friend


logger = logging.getLogger(__name__)

@csrf_exempt
@auth_user
@control_request_method(method=('GET', 'POST'))
def get_or_post_friend(request):

    user = request.user
    if request.method == 'GET':
        friends = Friend.objects.filter(user=user.id)
        data = FriendSerializer(
            friends, many=True, context={'user_id': user.id}
        ).data
        logger.info(f"friends serialized: {data}")
        return JsonResponse(
            data,
            status=200,
            safe=False
        )

    if request.method == 'POST':
        logger.info(f"{request.body}, {user}")
        data = json.loads(request.body)
        try:
            name = data['name']

        except:
            logger.error(tb.format_exc())
            return Response(
                {'name': 'This field is required.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        friend = Friend(
            user=user,
            name=name,
        )
        friend.save()
        data = {
            'friendId': friend.id,
            'count': count_events_for_friend(friend.id)
        }
        return JsonResponse(
            data,
            status=201,
            safe=False
        )

    return HttpResponse(
        content={'Not valid'},
        status=400
    )


@csrf_exempt
@auth_user
@control_request_method(method=('GET', 'DELETE', 'POST'))
def control_friend_info(request, pk):
    try:
        friend = Friend.objects.get(id=pk)

    except Friend.DoesNotExist:
        return HttpResponseNotFound(
            content={'Not found'},
        )

    except Friend.MultipleObjectsReturned:
        return HttpResponseBadRequest(
            content={'Too many objects'},
        )

    except:
        logger.error(tb.format_exc())
        return HttpResponseBadRequest(
            content={'Unknown error'},
        )

    if request.method == 'GET':
        try:
            data = FriendDetailSerializer(friend).data
            logger.info(f"friend serialized: {data}")

        except:
            logger.error(tb.format_exc())
            return HttpResponseBadRequest(
                content={'Unknown error'},
            )

        return JsonResponse(
            data,
            status=200,
            safe=False
        )

    if request.method == 'DELETE':
        try:
            friend.delete()

        except:
            logger.error(tb.format_exc())
            return HttpResponseBadRequest(
                content={'Unknown error'}
            )

        return HttpResponse(
            content={'Success'}, status=204
        )

    # if request.method == 'POST':
    #     try:
    #         data = json.loads(request.body)
    #         logger.info("data: %s", data)

    #     except:
    #         logger.error(tb.format_exc())
    #         return HttpResponseBadRequest(
    #             content={'Unknown error'}
    #         )

    #     return HttpResponse(
    #         content={'Success'},
    #         status=200
    #     )
