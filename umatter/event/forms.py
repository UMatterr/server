from django import forms

from .models import Event


class EventForm(forms.ModelForm):
    name = forms.CharField(
        max_length=250,
        required=True,
    )

    class Meta:
        model = Event
        fields = [
            'name',
            # 'phone_number', 'birthday',
        ]
