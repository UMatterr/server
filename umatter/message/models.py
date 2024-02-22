from django.db import models
from core.models import IDModel, TimestampModel


class Phrase(IDModel, TimestampModel):
    text = models.TextField(unique=True)

    class Meta:
        db_table = 'phrase'

    def __str__(self):
        return str(self.text, self.id)
