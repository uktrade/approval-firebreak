from django import forms

from .task import Task


class EmailForm(forms.Form):
    subject = forms.CharField()
    message = forms.CharField(widget=forms.Textarea)
    from_email = forms.EmailField()
    recipient_list = forms.CharField()


class EmailFormTask(Task, input="email_form"):
    auto = False
    form = EmailForm

    def execute(self, **kwargs):
        form = self.form(data=kwargs)

        if not form.is_valid():
            raise Exception(form.errors)

        return None, form.cleaned_data
