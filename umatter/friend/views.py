import logging

from django.http import HttpResponse

from user.utils import auth_user, control_request_method

from .forms import FriendForm
from .models import Friend
from .serializers import FriendSerializer


logger = logging.getLogger(__name__)

@auth_user
@control_request_method(method=('GET', 'POST'))
def get_or_post_friend(request):

    kakao_id = request.kakao_id
    access_token = request.access_token
    refresh_token = request.refresh_token
    logger.info(
        f"user kakao id: {kakao_id}, {access_token}, {refresh_token}"
    )
    if request.method == 'GET':
        friends = Friend.objects.all()
        data = FriendSerializer(friends, many=True).data
        logger.info(f"friends: {friends}")
        logger.info(f"friends serialized: {data}")
        return HttpResponse(
            content=data,
            status=200
        )

    if request.method == 'POST':
        logger.info(request.POST)
        form = FriendForm(request.POST)
        if form.is_valid():
            form.save()
            # friends = Friend.objects.all()
            # data = FriendSerializer(friends, many=True).data
            return HttpResponse(
                content={'Saved'},
                # content=data,
                status=201
            )

        return HttpResponse(
            content={'Not valid'},
            status=400
        )



@auth_user
@control_request_method()
def get_friend_info(request, uuid):
    try:
        friend = Friend.objects.get(id=uuid)
        data = FriendSerializer(friend, many=True).data
        logger.info(f"friend: {friend}")
        logger.info(f"friend serialized: {data}")

    except Friend.DoesNotExist:
        return HttpResponse(
            content={'Not found'},
            status=404
        )

    except Friend.MultipleObjectsReturned:
        return HttpResponse(
            content={'Too many objects'},
            status=404
        )

    return HttpResponse(content=data, status=200)


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
