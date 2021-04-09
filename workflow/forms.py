from django import forms
from django.forms.widgets import Textarea, Select, CheckboxInput,TextInput, DateInput

from workflow.models import (
    Requirement,
    RequirementSubmitStep,
    HiringManagerApprovalStep,
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
                widget.attrs.update({'class': 'govuk-checkboxes'})
            elif isinstance(widget, TextInput):
                widget.attrs.update({'class': 'govuk-input'})


class RejectForm(forms.Form):
    details = forms.CharField(
        widget=forms.Textarea(attrs={
            "rows": 5, "cols": 20,
            "class": "govuk-textarea",
        })
    )


class RequestChangesForm(forms.Form):
    details = forms.CharField(
        widget=forms.Textarea(attrs={
            "rows": 5, "cols": 20,
            "class": "govuk-textarea",
        })
    )


class ApprovalForm(forms.Form):
    approved = forms.BooleanField(
        required=True,
    )


class ChiefApprovalForm(ApprovalForm):
    def save(self, requirement):
        requirement.give_chief_approval()
        requirement.save()


class BusOpsApprovalForm(ApprovalForm):
    def save(self, requirement):
        requirement.give_chief_approval()
        requirement.save()


class DirectorApprovalForm(ApprovalForm):
    def save(self, requirement):
        requirement.give_chief_approval()
        requirement.save()


class DHCOOApprovalForm(ApprovalForm):
    def save(self, requirement):
        requirement.give_chief_approval()
        requirement.save()



class RequirementSubmitStepForm(GovFormattedModelForm):
    class Meta:
        model = RequirementSubmitStep
        fields = [
            "project_name_role_title",
            "IR35",
            "directorate",
            "name_of_hiring_manager",
            "email_of_hiring_manager",
            "authorising_director",
            "email_of_authorising_director",
            "new_requirement",
            "name_of_contractor",
            "uk_based",
            "overseas_country",
            "start_date",
            "end_date",
            "type_of_security_clearance",
            "contractor_type",
            "part_b_business_case",
            "part_b_impact",
            "part_b_main_reason",
            "job_description_submitted",
            "requirement",
        ]
        # exclude = ['requirement']

    def __init__(self, *args, **kwargs):
        self.submitter = kwargs.pop("submitter", None)
        super(RequirementSubmitStepForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        # Create a new requirement
        instance = super(
            RequirementSubmitStepForm,
            self,
        ).save(commit=False)
        instance.requirement = Requirement.objects.create(
            submitter=self.submitter,
        )
        instance.save()

        return instance


class HiringManagerApprovalStepForm(forms.ModelForm):
    class Meta:
        model = HiringManagerApprovalStep
        fields = [
            "cost_centre_code",
            "name_of_chief",
            "email_of_chief",
        ]

    def __init__(self, *args, **kwargs):
        self.requirement = kwargs.pop("requirement", None)
        super(HiringManagerApprovalStepForm, self).__init__(*args, **kwargs)
        self.fields['cost_centre_code'].widget.attrs.update({'class': 'govuk-input'})
        self.fields['name_of_chief'].widget.attrs.update({'class': 'govuk-input'})
        self.fields['email_of_chief'].widget.attrs.update({'class': 'govuk-input'})

    def save(self, commit=True):
        # Create a new requirement
        instance = super(
            HiringManagerApprovalStepForm,
            self,
        ).save(commit=False)
        instance.requirement = self.requirement
        instance.requirement.give_hiring_manager_approval(
            chief_email=instance.email_of_chief,
        )
        instance.requirement.save()
        instance.save()

        return instance
