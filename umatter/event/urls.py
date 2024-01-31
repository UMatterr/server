from django.urls import path

from .views import (
    get_or_post_event,
    delete_event,
)


urlpatterns = [
    path(
        route='',
        view=get_or_post_event,
        name='event'
    ),
    path(
        route='<str:uuid>',
        view=delete_event,
        name='delete_event'
    ),
]
