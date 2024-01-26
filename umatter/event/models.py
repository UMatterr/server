from django.db import models

from core.models import IDModel, TimestampModel
from friend.models import Friend


class EventType(IDModel):
    name = models.CharField(
        max_length=255,
    )

    class Meta:
        db_table = 'event_type'


class Event(IDModel, TimestampModel):
    name = models.CharField(
        max_length=255,
    )
    friend = models.ManyToManyField(
        Friend,
    )
    event_type = models.ManyToManyField(
        EventType,
    )
    send_msg_at = models.DateTimeField(
        null=True,
    )
    repeat_cycle = models.IntegerField()

    class Meta:
        db_table = 'event'
