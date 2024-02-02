from django.core.validators import MaxLengthValidator
from django.db import models

from core.models import IDModel, PhoneModel, TimestampModel
from user.models import User


class Friend(IDModel, PhoneModel, TimestampModel):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        db_column='user',
    )
    name = models.CharField(
        max_length=250,
        validators=[MaxLengthValidator(250)],
    )
    birthday = models.DateField(
        null=True,
    )

    class Meta:
        db_table = 'friend'
