import json
import logging
import traceback as tb

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from rest_framework import status
from rest_framework.response import Response

from user.utils import auth_user, control_request_method

from .forms import FriendForm
from .models import Friend
from .serializers import FriendSerializer


logger = logging.getLogger(__name__)

@csrf_exempt
@auth_user
@control_request_method(method=('GET', 'POST'))
def get_or_post_friend(request):

    kakao_id = request.user
    access_token = request.COOKIES.get('access_token')
    refresh_token = request.COOKIES.get('refresh_token')
    logger.info(
        f"user kakao id: {kakao_id}, {access_token}, {refresh_token}"
    )
    user = request.user
    if request.method == 'GET':
        friends = Friend.objects.filter(user_id=user.id)
        data = FriendSerializer(friends, many=True).data
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
            user_id=user.id,
            name=name,
        )
        friend.save()
        friends = Friend.objects.filter(
            user_id=user.id
        )
        data = FriendSerializer(friends, many=True).data
        logger.info(f"Updated friends: {data}")
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
@control_request_method()
def get_friend_info(request, uuid):
    try:
        friend = Friend.objects.get(id=uuid)
        data = FriendSerializer(friend, many=True).data
        logger.info(f"friend: {friend}")
        logger.info(f"friend serialized: {data}")

    except Friend.DoesNotExist:
        # return HttpResponse(
        #     content={'Not found'},
        #     status=404
        # )
        return Response(
            {'Not found'},
            status=status.HTTP_404_NOT_FOUND
        )

    except Friend.MultipleObjectsReturned:
        # return HttpResponse(
        #     content={'Too many objects'},
        #     status=404
        # )
        return Response(
            {'Not found'},
            status=status.HTTP_404_NOT_FOUND
        )

    # return HttpResponse(content=data, status=200)
    return Response(
        data,
        status=status.HTTP_200_OK
    )


@csrf_exempt
@auth_user
@control_request_method(method=('POST'))
def update_friend_info(request, uuid):
    try:
        friend = Friend.objects.get(id=uuid)
        data = FriendSerializer(friend, many=True).data
        logger.info(f"friend: {friend}")
        logger.info(f"friend serialized: {data}")

    except Friend.DoesNotExist:
        return HttpResponse(
            content={'Not found'}, status=404
        )

    except Friend.MultipleObjectsReturned:
        return HttpResponse(
            content={'Too many objects'}, status=404
        )

    return HttpResponse(content=data, status=200)


@csrf_exempt
@auth_user
@control_request_method(method=('DELETE'))
def delete_friend(request, uuid):
    try:
        friend = Friend.objects.get(id=uuid)
        logger.info(f"friend to delete: {friend}")
        friend.delete()

    except Friend.DoesNotExist:
        return HttpResponse(
            content={'Not found'}, status=404
        )

    except Friend.MultipleObjectsReturned:
        return HttpResponse(
            content={'Too many objects'}, status=404
        )

    return HttpResponse(
        content={'Success'}, status=200
    )
