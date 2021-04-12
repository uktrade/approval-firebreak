from datetime import date

from django import forms


class DateSelectorWidget(forms.MultiWidget):
    def __init__(self, attrs=None):
        widgets = [
            forms.NumberInput(
                attrs={
                    'class': 'govuk-date-input__item govuk-input govuk-input--width-2',
                    'placeholder': 'DD'}),
            forms.NumberInput(
                attrs={
                    'class': 'govuk-date-input__item govuk-input govuk-input--width-2',
                    'placeholder': 'MM'}),
            forms.NumberInput(
                attrs={
                    'class': 'govuk-date-input__item govuk-input govuk-input--width-3',
                    'placeholder': 'YYYY'}),
        ]
        super().__init__(widgets, attrs)

    def decompress(self, value):
        if isinstance(value, date):
            return [value.day, value.month, value.year]
        elif isinstance(value, str):
            year, month, day = value.split('-')
            return [day, month, year]
        return [None, None, None]

    def value_from_datadict(self, data, files, name):
        day, month, year = super().value_from_datadict(data, files, name)
        return '{}-{}-{}'.format(year, month, day)
