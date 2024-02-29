from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include, path

from core.views import health_check
from event.views import get_events, create_event, delete_event, get_event_type
from friend.views import get_or_post_friend
from message.views import post_converted_phrase, put_message

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('user.urls')),
    path('healthz', health_check, name='health_check'),

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

    # swagger
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
] + staticfiles_urlpatterns()
