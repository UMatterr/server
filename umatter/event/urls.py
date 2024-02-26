from django.urls import path

from .views import (
    get_event_by_friend,
)


urlpatterns = [
    path(
        route='<uuid:pk>',
        view=get_event_by_friend,
        name='get_event_by_friend'
    ),
]
