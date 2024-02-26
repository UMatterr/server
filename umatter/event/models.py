from django.core.validators import MaxLengthValidator
from django.db import models

from core.models import IDModel, TimestampModel
from friend.models import Friend
from user.models import User


class EventType(models.Model):
    id = models.AutoField(
        primary_key=True,
        editable=False
    )
    name = models.CharField(
        max_length=100,
        validators=[MaxLengthValidator(100)],
    )

    class Meta:
        db_table = 'event_type'
        ordering = ['id']


class Event(IDModel, TimestampModel):
    name = models.CharField(
        max_length=250,
        validators=[MaxLengthValidator(250)],
    )
    user = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        db_column='user',
    )
    friend = models.ForeignKey(
        Friend,
        on_delete=models.CASCADE,
        null=True,
        db_column='friend',
    )
    event_type = models.ForeignKey(
        EventType,
        on_delete=models.DO_NOTHING,
        db_column='event_type',
    )
    date = models.DateField(
        null=True,
    )
    repeat = models.IntegerField(
        null=True,
    )

    class Meta:
        db_table = 'event'
        ordering = ['friend__name', 'event_type__id']
