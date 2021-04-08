from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from django.urls import reverse
from django.http import Http404

from workflow.forms import (
    ChiefApproval,
    RequirementFinanceStep,
    RequirementSubmitStepForm,
)
from workflow.models import Requirement


# New requirement
class NewRequirementView(View):
    form_class = RequirementSubmitStepForm
    template_name = 'new_requirement.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            # TODO - send message to CHIEF
            return HttpResponseRedirect(
                reverse("requirement_submitted")
            )

        return render(request, self.template_name, {'form': form})


class RequirementSubmittedView(View):
    form_class = RequirementSubmitStepForm
    template_name = 'requirement_submitted.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


def get_form_and_template(requirement, content):
    if requirement.state == "submitted":
        # Needs Chief approval
        form = ChiefApproval(content)
        template_name = "chief_approval.html"
        success_view = "chief_approved"
    elif requirement.state == "in_progress":
        form = RequirementFinanceStep(content)
        template_name = "finance_approval.html"
        success_view = "finance_approved"

    return form, template_name, success_view


# Approval
class ApprovalView(View):
    def get(self, request, *args, **kwargs):
        requirement_id = self.kwargs['requirement_id']
        requirement = Requirement.objects.filter(
            uuid=requirement_id,
        ).first()

        if not requirement:
            raise Http404("Cannot find requirement")

        form, template_name, _ = get_form_and_template(requirement)

        return render(request, template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        requirement_id = self.kwargs['requirement_id']
        requirement = Requirement.objects.filter(
            uuid=requirement_id,
        ).first()

        if not requirement:
            raise Http404("Cannot find requirement")

        form, template_name, success_view = get_form_and_template(
            requirement,
            request.POST,
        )

        if form.is_valid():
            form.save(requirement)
            return HttpResponseRedirect(
                reverse(success_view)
            )

        return render(
            request,
            self.template_name,
            {'form': form}
        )
