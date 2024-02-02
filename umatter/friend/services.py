import logging
import traceback as tb

from event.models import Event

logger = logging.getLogger(__name__)


def count_events_for_friend(pk):
    try:
        return Event.objects.filter(friend__id=pk).count()

    except Exception as e:
        logger.error("%s, %s", e, tb.format_exc())
        return 0
