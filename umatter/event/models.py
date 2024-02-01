from django.core.validators import MaxLengthValidator
from django.db import models

from core.models import IDModel, TimestampModel
from friend.models import Friend


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


class CustomEventType(models.Model):
    id = models.AutoField(
        primary_key=True,
        editable=False
    )
    name = models.CharField(
        max_length=100,
        validators=[MaxLengthValidator(100)],
        unique=True,
    )

    class Meta:
        db_table = 'custom_event_type'


class Event(IDModel, TimestampModel):
    name = models.CharField(
        max_length=250,
        validators=[MaxLengthValidator(250)],
    )
    friend = models.ForeignKey(
        Friend,
        on_delete=models.CASCADE,
        null=True,
    )
    event_type = models.ManyToManyField(
        EventType,
    )
    custom_event_type = models.ForeignKey(
        CustomEventType,
        on_delete=models.DO_NOTHING,
        null=True,
    )
    date = models.DateField(
        null=True,
    )
    repeat = models.IntegerField(
        null=True,
    )

    class Meta:
        db_table = 'event'
