from django import forms
from django.core.exceptions import ValidationError
from django.forms.widgets import DateInput
from django.utils.translation import gettext_lazy as _

from .models import Friend


class FriendForm(forms.ModelForm):
    name = forms.CharField(
        max_length=250,
        required=False,
    )

    class Meta:
        model = Friend
        fields = [
            'name',
        ]
        labels = {
            'name': _('Name'),
        }
        help_texts = {
            'name': _('Name of the friend'),
        }
        error_messages = {
            'name': {
                'max_length': _('Name must be less than 250 characters'),
            },
        }
