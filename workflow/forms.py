from django import forms

from workflow.models import (
    RequirementSubmitStep,
    RequirementFinanceStep,
)


class ApprovalForm(forms.Form):
    approved = forms.BooleanField(
        required=True,
    )


class ChiefApproval(ApprovalForm):
    def save(self, requirement):
        requirement.give_chief_approval()
        requirement.save()


class RequirementSubmitStepForm(forms.ModelForm):
    class Meta:
        model = RequirementSubmitStep
        fields = "__all__"
    #
    # def save(self, commit=True):
    #     instance = super(
    #         RequirementSubmitStepForm,
    #         self,
    #     ).save(commit=True)



class RequirementFinanceStepForm(forms.ModelForm):
     class Meta:
         model = RequirementFinanceStep
         fields = "__all__"