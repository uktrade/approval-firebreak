from django import forms

from workflow.models import (
    Requirement,
    RequirementSubmitStep,
    HiringManagerApprovalStep,
)


class RejectForm(forms.Form):
    details = forms.CharField(widget=forms.Textarea(attrs={"rows":5, "cols":20}))


class RequestChangesForm(forms.Form):
    details = forms.CharField(widget=forms.Textarea(attrs={"rows":5, "cols":20}))


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


class RequirementSubmitStepForm(forms.ModelForm):
    class Meta:
        model = RequirementSubmitStep
        fields = [
            "name_of_hiring_manager",
            "email_of_hiring_manager",
        ]

    def __init__(self, *args, **kwargs):
        self.submitter = kwargs.pop("submitter", None)
        super(RequirementSubmitStepForm, self).__init__(*args, **kwargs)
        self.fields['name_of_hiring_manager'].widget.attrs.update({'class': 'govuk-input'})
        self.fields['email_of_hiring_manager'].widget.attrs.update({'class': 'govuk-input'})

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
