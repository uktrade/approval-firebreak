from django import forms

from recruitment_approval.models import Requirement
from workflow.tasks import Task


class HiringManagerApprovalForm(forms.Form):
    approved = forms.BooleanField(
        required=False,
        label="I approve this requirement",
        widget=forms.CheckboxInput(),
    )
    rejection_reason = forms.CharField(widget=forms.Textarea)


class HiringManagerApproval(Task, input="hiring_manager_approval"):
    auto = False
    form = HiringManagerApprovalForm
    template = "recruitment_approval/approval.html"

    def execute(self, task_info):
        form = self.form(task_info)

        if not form.is_valid():
            # TODO: how to display form with errors
            raise Exception(form.errors)

        target = (
            "hiring_approved" if form.cleaned_data["approved"] else "hiring_rejected"
        )

        return target, form.cleaned_data

    def context(self):
        requirement = Requirement.objects.get(pk=self.flow.flow_info["requirement_id"])

        return {
            "requirement": requirement,
            "form": self.form(initial=self.task_record.task_info),
        }
