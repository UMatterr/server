from django.urls import path

from .views import (
    get_phrase,
)


urlpatterns = [
    path(
        route='<str:event_id>',
        view=get_phrase,
        name='get_phrase',
    ),
]
