from django.urls import path

from .views import (
    get_or_post_friend,
)


urlpatterns = [
    path(
        route='',
        view=get_or_post_friend,
        name='friends'
    ),
]
