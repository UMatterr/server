from django.urls import path

from .views import (
    get_friend_info,
)


urlpatterns = [
    path(
        route='<uuid:pk>',
        view=get_friend_info,
        name='get_friend_info'
    ),
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
