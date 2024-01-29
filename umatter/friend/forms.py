from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .models import Friend


class FriendForm(forms.ModelForm):
    name = forms.CharField(
        max_length=250,
        required=False,
    )
    phone_number = forms.CharField(
        max_length=250,
        required=False,
    )
    birthday = forms.DateField(required=False)
