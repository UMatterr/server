"""
URL configuration for umatter project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path

from event.views import get_events, create_event, delete_event, get_event_type
from friend.views import get_or_post_friend
from message.views import post_converted_phrase, put_message


urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('user.urls')),

    # event
    path('etype', get_event_type, name='get_event_type'),
    path('event', create_event, name='create_event'),
    path('event/<uuid:pk>', delete_event, name='delete_event'),
    path('events', get_events, name='get_events'),
    path('events/', include('event.urls')),

    # friend
    path('friends', get_or_post_friend, name='friends'),
    path('friends/', include('friend.urls')),

    # message
    path('converted/',post_converted_phrase, name='post_converted_phrase'),
    path('phrase/', include('message.urls')),
    path('message', put_message, name='put_message'),
]
