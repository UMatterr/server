from django.urls import path

from .views import (
    EventDetailView,
    EventListView,
    EventTypeDetailView,
    EventTypeListView,
)


urlpatterns = [
    path(
        route='',
        view=EventListView.as_view(),
        name='event_list'
    ),
    path(
        route='info/<uuid>',
        view=EventDetailView.as_view(),
        name='event_detail'
    ),
    path(
        route='types',
        view=EventTypeListView.as_view(),
        name='event_type_list'
    ),
    path(
        route='type/<uuid>',
        view=EventTypeDetailView.as_view(),
        name='event_type_detail'
    ),
]

