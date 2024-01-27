from django.urls import path

from .views import (
    FriendView,
    FriendListView,
)


urlpatterns = [
    path(
        route='',
        view=FriendListView.as_view(),
        name='friend_list'
    ),
    path(
        route='info/<uuid>',
        view=FriendView.as_view(),
        name='friend_detail'
    ),
]
