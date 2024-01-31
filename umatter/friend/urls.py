from django.urls import path

from .views import (
    get_or_post_friend,
)


urlpatterns = [
    path(
        route='',
        view=get_or_post_friend,
        name='friends'
    ),
    # path(
    #     route='<str:uuid>',
    #     view=get_friend_info,
    #     name='get_friend_info'
    # ),
    # path(
    #     route='<str:uuid>',
    #     view=update_friend_info,
    #     name='update_friend_info'
    # ),
    # path(
    #     route='<str:uuid>',
    #     view=delete_friend,
    #     name='delete_friend'
    # ),
]
