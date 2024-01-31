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
    # phone_number = forms.CharField(
    #     max_length=250,
    #     required=False,
    # )
    # birthday = forms.DateField(
    #     required=False
    # )

    class Meta:
        model = Friend
        fields = [
            'name',
            # 'phone_number', 'birthday',
        ]
        # widgets = {
        #     'birthday': DateInput(
        #         format=('%Y/%m/%d'),
        #         attrs={
        #             'class': 'form-control',
        #             'placeholder': 'Select a date',
        #             'type': 'date',
        #         }
        #     ),
        # }
        labels = {
            'name': _('Name'),
            # 'phone_number': _('Phone Number'),
            # 'birthday': _('Birthday'),
        }
        help_texts = {
            'name': _('Name of the friend'),
            # 'phone_number': _('Phone number of the friend'),
            # 'birthday': _('Birthday of the friend'),
        }
        error_messages = {
            'name': {
                'max_length': _('Name must be less than 250 characters'),
            },
            # 'phone_number': {
            #     'max_length': _('Phone number must be less than 250 characters'),
            # },
            # 'birthday': {
            #     'invalid': _('Birthday must be a valid date'),
            # },
        }
