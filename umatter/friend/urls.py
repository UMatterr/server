from django.urls import path

from .views import (
    FriendDetailView,
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
        view=FriendDetailView.as_view(),
        name='friend_detail'
    ),
]
