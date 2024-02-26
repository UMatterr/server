import logging

from .models import EventType


logger = logging.getLogger(__name__)

def is_valid_event_type(event_type):
    try:
        return EventType.objects.filter(id=int(event_type)).exists()

    except Exception as e:
        logger.error("is_vaild_event_type: %s", e, exc_info=True)
