import re
from datetime import datetime

from django import forms
from django.core.exceptions import ValidationError
from django.forms import NumberInput, TextInput, EmailInput
from .models import Booking


class DateInput(forms.DateInput):
    input_type = 'date'


class BookForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['date_from', 'date_to', 'guests']
        widgets = {
            'date_from': DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'date_to': DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'guests': NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'max': 4
            }),
        }

    def clean(self):
        date_from = self.cleaned_data.get('date_from')
        date_to = self.cleaned_data.get('date_to')
        date_now = datetime.today().date()
        date_limit_str = '2021-12-31'
        date_limit = datetime.strptime(date_limit_str, '%Y-%m-%d').date()
        errors = {}

        if date_from == date_to:
            errors['date_to'] = 'Check-out date cannot be equal to check-in date'
        if date_from > date_to:
            errors['date_to'] = 'Check-out date cannot be earlier than check-in date'
        if date_from < date_now:
            errors['date_from'] = 'Check-in date cannot be earlier than today'
        if date_to > date_limit:
            errors['date_to'] = 'Reservations are currently only available until {0}'.format(date_limit_str)
        if date_from > date_limit:
            errors['date_from'] = 'Reservations are currently only available until {0}'.format(date_limit_str)

        if errors:
            raise ValidationError(errors)
        return self.cleaned_data


class ConfirmationForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['contact_name', 'contact_email', 'contact_phone']
        widgets = {
            'contact_name': TextInput(attrs={
                'class': 'form-control',
            }),
            'contact_email': EmailInput(attrs={
                'class': 'form-control'
            }),
            'contact_phone': TextInput(attrs={
                'class': 'form-control'
            }),
        }

    def clean(self):
        contact_phone = self.cleaned_data.get('contact_phone')
        errors = {}
        pattern = re.compile('[0-9]{9}')

        if not pattern.match(contact_phone):
            errors['contact_phone'] = 'Invalid phone number'

        if errors:
            raise ValidationError(errors)
        return self.cleaned_data
