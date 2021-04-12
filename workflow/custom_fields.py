from django.db import models
from django import forms


class YesNoBooleanField(forms.BooleanField):
    widget = forms.RadioSelect(choices=(
        (True,"Yes"),
        (False, "No")))


class YesNoField(models.BooleanField):
    widget = forms.RadioSelect

    def formfield(self, **kwargs):
        if self.choices is not None:
            include_blank = not (self.has_default() or 'initial' in kwargs)
            defaults = {'choices': self.get_choices(include_blank=include_blank)}
        else:
            form_class = YesNoBooleanField if self.null else YesNoBooleanField
            defaults = {'form_class': form_class, 'required': False}
        return super().formfield(**{**defaults, **kwargs})

