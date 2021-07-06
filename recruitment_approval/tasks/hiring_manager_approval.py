from django import forms
from django.core.exceptions import ValidationError

from recruitment_approval.models import Requirement
from workflow.forms import GovFormattedForm
from workflow.tasks import Task, TaskError


class HiringManagerApprovalForm(GovFormattedForm):
    approved = forms.BooleanField(
        required=False,
        label="I approve this requirement",
        widget=forms.CheckboxInput(),
    )
    rejection_reason = forms.CharField(widget=forms.Textarea, required=False)

    def clean(self):
        cleaned_data = super().clean()
        approved = cleaned_data.get("approved")
        rejection_reason = cleaned_data.get("rejection_reason")

        if not approved and not rejection_reason:
            raise ValidationError(
                "You must supply a rejection reason " "when rejecting a requirement"
            )


class HiringManagerApproval(Task, input="hiring_manager_approval"):
    auto = False
    form = HiringManagerApprovalForm
    template = "recruitment_approval/approval.html"

    def execute(self, task_info):
        form = self.form(task_info)

        if not form.is_valid():
            # TODO: how to display form with errors
            raise TaskError("Form is not valid", {"form": form})

        self.flow.flow_info["rejection_reason"] = form.cleaned_data.get(
            "rejection_reason"
        )

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
