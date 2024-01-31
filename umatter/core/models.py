import uuid

from django.core.validators import RegexValidator
from django.db import models


class IDModel(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    class Meta:
        abstract = True


class PhoneModel(models.Model):
    phone_regex = RegexValidator(
        # regex=r'^\+?[\d]{0,3}\s?\d{2,3}[-\s]?\d{3,4}[-\s]?\d{4}$',
        regex=r'^\d{2,3}[-\s]\d{3,4}[-\s]\d{4}$',
        message='''
            Phone number must be entered in the one of the following formats:
            010-7890-1234
            01078901234
            027891234
            02-789-1234
            02 789 1234
            02 7890 1234
            02-7890-1234
            032-789-1234
            032-7890-1234
            03278901234
        ''',
    )
    phone_number = models.CharField(
        validators=[phone_regex],
        max_length=17,
        blank=True,
    )

    class Meta:
        abstract = True


class TimestampModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
