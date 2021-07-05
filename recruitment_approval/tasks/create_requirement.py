from django import forms
from django.forms.widgets import (
    Textarea,
    Select,
    CheckboxInput,
    TextInput,
    DateInput,
    EmailInput,
)

from recruitment_approval.models import Requirement

from workflow.tasks import Task


class GovFormattedModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(forms.ModelForm, self).__init__(*args, **kwargs)
        for field in self.fields.items():
            widget = field[1].widget
            if isinstance(widget, Textarea):
                widget.attrs.update({"class": "govuk-textarea"})
            elif isinstance(widget, Select):
                widget.attrs.update({"class": "govuk-select"})
            elif isinstance(widget, CheckboxInput):
                widget.attrs.update({"class": "govuk-checkboxes__input"})
            elif isinstance(widget, TextInput) or isinstance(widget, EmailInput):
                widget.attrs.update({"class": "govuk-input"})


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
            "start_date": DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
            "end_date": DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
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

        if self.hiring_manager:
            instance.hiring_manager = self.hiring_manager

        instance.save()

        return instance


class CreateRequirement(Task, input="create_requirement"):
    auto = False
    form = NewRequirementForm

    def execute(self, task_info):
        form = self.form(task_info, hiring_manager=self.user)

        if form.is_valid():
            form.save()
        else:
            raise Exception(form.errors)

        self.flow.flow_info["requirement_id"] = str(form.instance.pk)
        self.flow.flow_info["requirement_url"] = "https://www.google.com"

        return None, form.cleaned_data

    def context(self):
        return {"form": self.form(initial=self.task_record.task_info)}


class ReviewRequirement(Task, input="review_requirement"):
    auto = False
    form = NewRequirementForm

    def execute(self, task_info):
        requirement = Requirement.objects.get(pk=self.flow.flow_info["requirement_id"])

        form = self.form(instance=requirement, data=task_info)

        if form.is_valid():
            form.save()
        else:
            raise Exception(form.errors)

        return "hiring_manager_approval", form.cleaned_data

    def context(self):
        requirement = Requirement.objects.get(pk=self.flow.flow_info["requirement_id"])

        return {"form": self.form(instance=requirement)}
