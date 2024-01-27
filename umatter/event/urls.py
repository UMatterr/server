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
        route='info/<str:uuid>',
        view=EventDetailView.as_view(),
        name='event_detail'
    ),
    path(
        route='types',
        view=EventTypeListView.as_view(),
        name='event_type_list'
    ),
    path(
        route='type/<str:uuid>',
        view=EventTypeDetailView.as_view(),
        name='event_type_detail'
    ),
]

