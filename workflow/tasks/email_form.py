from django import forms

from .task import Task


class EmailForm(forms.Form):
    subject = forms.CharField()


class EmailFormTask(Task, input="email_form"):
    auto = False
    form = EmailForm

    def execute(self, **kwargs):
        form = self.form(data=kwargs)

        if not form.is_valid():
            raise Exception

        return None, form.cleaned_data
