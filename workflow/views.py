from django.http import HttpResponseRedirect
from django.http import Http404
from django.shortcuts import render
from django.urls import reverse
from django.views import View
from django.views.generic.list import ListView
from django.conf import settings

from core.notify import send_email

from workflow.forms import (
    ChiefApprovalForm,
    HiringManagerApprovalStepForm,
    RejectForm,
    RequirementSubmitStepForm,
    RequestChangesForm,
)
from workflow.models import Requirement


# New requirement
class RequirementsView(ListView):
    template_name = 'requirements.html'
    model = Requirement
    paginate_by = 1000  # if pagination is desired

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


# New requirement
class NewRequirementView(View):
    form_class = RequirementSubmitStepForm
    template_name = 'new_requirement.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, submitter=request.user)
        if form.is_valid():
            requirement_submit_step = form.save()

            # Email Hiring manager
            send_email(
                to=requirement_submit_step.email_of_hiring_manager,
                template_id=settings.HIRING_MANAGER_NEW_REQUEST_TEMPLATE_ID,
                personalisation={
                    "submitter_name": request.user.get_full_name(),
                },
            )

            return HttpResponseRedirect(
                reverse("requirement_submitted")
            )

        return render(request, self.template_name, {'form': form})


class RequirementSubmittedView(View):
    form_class = RequirementSubmitStepForm
    template_name = 'requirement_submitted.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


def get_form_and_template(requirement, content=None):
    if requirement.state == "submitted":
        # Needs Chief approval
        form = HiringManagerApprovalStepForm(content, requirement=requirement)
        template_name = "hiring_manager_approval.html"
        success_view = "approved"
    elif requirement.state == "submitted":
        # Needs Chief approval
        form = ChiefApprovalForm(content, requirement=requirement)
        template_name = "chief_approval.html"
        success_view = "approved"
    # elif requirement.state == "in_progress":
    #     form = RequirementFinanceStepForm(content)
    #     template_name = "finance_approval.html"
    #     success_view = "approved"

    return form, template_name, success_view


# Approval
class ApprovalView(View):
    def get(self, request, *args, **kwargs):
        requirement_id = self.kwargs['requirement_id']
        requirement = Requirement.objects.filter(
            uuid=requirement_id,
        ).first()

        request_changes_form = RequestChangesForm()
        reject_form = RejectForm()

        if not requirement:
            raise Http404("Cannot find requirement")

        form, template_name, _ = get_form_and_template(requirement)

        return render(request, template_name, {
            'form': form,
            "request_changes_form": request_changes_form,
            "reject_form": reject_form,
            'requirement': requirement,
        })

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

        return render(request, self.template_name, {
            'form': form,
            'requirement': requirement,
        })


class ApprovedView(View):
    template_name = 'approved.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
