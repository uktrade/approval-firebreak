from django.forms.widgets import DateInput

from recruitment_approval.models import Requirement

from workflow.forms import GovFormattedModelForm
from workflow.tasks import Task, TaskError


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
    form_class = NewRequirementForm

    def execute(self, task_info):
        form = self.form_class(task_info, hiring_manager=self.user)

        if form.is_valid():
            form.save()
        else:
            raise TaskError("Form is not valid", {"form": form})

        self.flow.flow_info["requirement_id"] = str(form.instance.pk)

        return None, form.cleaned_data

    def context(self):
        return {"form": self.form_class(initial=self.task_record.task_info)}


class ReviewRequirement(Task, input="review_requirement"):
    auto = False
    form_class = NewRequirementForm

    def execute(self, task_info):
        requirement = Requirement.objects.get(pk=self.flow.flow_info["requirement_id"])

        form = self.form_class(instance=requirement, data=task_info)

        if form.is_valid():
            form.save()
        else:
            raise TaskError("Form is not valid", {"form": form})

        return None, form.cleaned_data

    def context(self):
        requirement = Requirement.objects.get(pk=self.flow.flow_info["requirement_id"])

        return {"form": self.form_class(instance=requirement)}
