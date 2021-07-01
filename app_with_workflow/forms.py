from django import forms


class ApproveRequirementForm(forms.Form):
    pass


class DeclineRequirementForm(forms.Form):
    message = forms.CharField(
        widget=forms.Textarea(attrs={
            "rows": 5, "cols": 20,
            "class": "govuk-textarea",
        })
    )
