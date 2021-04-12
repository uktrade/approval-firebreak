from django import forms
from django.forms.widgets import Textarea, Select, CheckboxInput,TextInput, DateInput, EmailInput

from workflow.models import (
    Requirement,
)


class GovFormattedModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(forms.ModelForm, self).__init__(*args, **kwargs)
        for field in self.fields.items():
            widget = field[1].widget
            if isinstance(widget, Textarea):
                widget.attrs.update({'class': 'govuk-textarea'})
            elif isinstance(widget, Select):
                widget.attrs.update({'class': 'govuk-select'})
            elif isinstance(widget, CheckboxInput):
                widget.attrs.update({'class': 'govuk-checkboxes__input'})
            elif isinstance(widget, TextInput) or isinstance(widget, EmailInput):
                widget.attrs.update({'class': 'govuk-input'})


class RequestChangesForm(forms.Form):
    message = forms.CharField(
        widget=forms.Textarea(attrs={
            "rows": 5, "cols": 20,
            "class": "govuk-textarea",
        })
    )


class ApprovalForm(forms.Form):
    approved = forms.BooleanField(
        required=True,
        label="I approve this requirement",
        widget=forms.CheckboxInput(attrs={
            "class": "govuk-checkboxes__input",
        })
    )


class ChiefApprovalForm(ApprovalForm):
    def save(self, requirement):
        requirement.give_chief_approval()
        requirement.save()


class BusOpsApprovalForm(ApprovalForm):
    def save(self, requirement):
        requirement.give_busops_approval()
        requirement.save()


class DirectorApprovalForm(ApprovalForm):
    def save(self, requirement):
        requirement.give_chief_approval()
        requirement.save()


class DHCOOApprovalForm(ApprovalForm):
    def save(self, requirement):
        requirement.give_chief_approval()
        requirement.save()


class NewRequirementForm(GovFormattedModelForm):
    class Meta:
        model = Requirement
        fields = [
            "project_name_role_title",
            "group",
            "directorate",
            "cost_centre_code",
            "IR35",
            "new_requirement",
            "name_of_contractor",
            "contractor_type",
            "uk_based",
            "overseas_country",
            "start_date",
            "end_date",
            "type_of_security_clearance",
            "part_b_business_case",
            "part_b_impact",
            "part_b_main_reason",
            "job_description_submitted",
        ]
        widgets = {
            'start_date': DateInput(attrs={'type': 'date'}),
            'end_date': DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        self.hiring_manager = kwargs.pop("hiring_manager", None)
        super(NewRequirementForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        # Create a new requirement
        instance = super(
            NewRequirementForm,
            self,
        ).save(commit=False)
        instance.hiring_manager = self.hiring_manager
        instance.save()

        return instance
