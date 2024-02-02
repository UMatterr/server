import logging
import traceback as tb

from event.models import Event

logger = logging.getLogger(__name__)


def count_events_for_friend(friend_pk, user_pk):
    try:
        return Event.objects.filter(
            friend__id=friend_pk,
            user__id=user_pk
        ).count()

    except Exception as e:
        logger.error("%s, %s", e, tb.format_exc())
        return 0
