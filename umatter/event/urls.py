from django.urls import path

from .views import (
    delete_event,
    get_event_by_friend,
)


urlpatterns = [
    path(
        route='<uuid:pk>',
        view=get_event_by_friend,
        name='get_event_by_friend'
    ),
    path(
        route='rm/<uuid:pk>',
        view=delete_event,
        name='delete_event'
    ),
]
