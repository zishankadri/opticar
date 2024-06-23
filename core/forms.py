from django import forms
from django.utils.safestring import mark_safe

from .models import Car


class CarFilterForm(forms.Form):
    seats = forms.MultipleChoiceField(
        choices= Car.SEATS_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    make_and_model = forms.MultipleChoiceField(
        choices=Car.MAKE_AND_MODEL_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    car_type = forms.MultipleChoiceField(
        choices=Car.CAR_TYPE_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False
    )