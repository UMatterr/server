from django.urls import path

from .views import (
    control_friend_info,
)


urlpatterns = [
    path(
        route='<uuid:pk>',
        view=control_friend_info,
        name='control_friend_info'
    ),
]
