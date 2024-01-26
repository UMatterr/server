from django.db import models

from core.models import IDModel, TimestampModel
from user.models import User


class Friend(IDModel, TimestampModel):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    name = models.CharField(
        max_length=255,
    )
    phone_number = models.CharField(
        max_length=20,
        null=True,
    )
    birthday = models.DateField(
        null=True,
    )

    class Meta:
        db_table = 'friend'
