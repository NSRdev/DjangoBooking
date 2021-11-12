from django import forms
from django.forms import NumberInput

from .models import Booking


class DateInput(forms.DateInput):
    input_type = 'date'


class BookForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['date_from', 'date_to', 'guests' ]
        widgets = {
            'date_from': DateInput(attrs={
                'class': 'form-control'
            }),
            'date_to': DateInput(attrs={
                'class': 'form-control'
            }),
            'guests': NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Number of guests',
            }),
        }