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
    RequestChangesForm,
    NewRequirementForm,
)
from workflow.models import (
    Requirement,
    SUBMITTED,
    CHIEF_APPROVAL_REQUIRED,
    BUS_OPS_APPROVAL_REQUIRED,
    IN_PROGRESS,
    DIRECTOR_APPROVED,
    DG_COO_APPROVED,
    COMPLETE,
    REQUIREMENT_STATES,
)

in_progress_perms = [
    "can_give_commercial_approval",
    "can_give_finance_approval",
    "can_give_hr_approval",
]


# New requirement
class RequirementsView(ListView):
    template_name = 'requirements.html'
    model = Requirement
    paginate_by = 1000  # if pagination is desired

    def get_queryset(self):
        requirements = Requirement.objects.filter(
            #state=SUBMITTED,
            submitter=self.request.user,
        )

        if self.request.user.has_perm(
            "workflow.can_give_hiring_manager_approval"
        ):
            requirements = Requirement.objects.filter(
                state=SUBMITTED
            )
        elif self.request.user.has_perm(
            "workflow.can_give_chief_approval"
        ):
            requirements = Requirement.objects.filter(
                state=CHIEF_APPROVAL_REQUIRED
            )
        elif self.request.user.has_perm(
            "workflow.can_give_bus_ops_approval"
        ):
            requirements = Requirement.objects.filter(
                state=BUS_OPS_APPROVAL_REQUIRED
            )
        elif len([perm for perm in self.request.user.get_user_permissions() if perm in in_progress_perms]) > 0:
            requirements = Requirement.objects.filter(
                state=IN_PROGRESS
            )

        return requirements

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


# New requirement
class NewRequirementView(View):
    form_class = NewRequirementForm
    template_name = 'new_requirement.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        # TODO - check that user is in hiring manager group
        form = self.form_class(request.POST, hiring_manager=request.user)
        if form.is_valid():
            requirement = form.save()

            # Email Hiring manager
            send_email(
                to=requirement.hiring_manager.email,
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
    template_name = 'requirement_submitted.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


def get_form_and_template(requirement, content=None):
    if requirement.state == CHIEF_APPROVAL_REQUIRED:
        # Needs Chief approval
        form = ChiefApprovalForm(content)
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

        requirement_state = REQUIREMENT_STATES[requirement.state]
        found_perm = False

        for permission in requirement_state["permissions"]:
            if request.user.has_perm(f"workflow.{permission}"):
                found_perm = True
                break

        if not found_perm:
            return HttpResponseRedirect(
                reverse(
                    "needs_auth",
                    kwargs={"requirement_id": requirement_id}
                )
            )

        request_changes_form = RequestChangesForm()

        if not requirement:
            raise Http404("Cannot find requirement")

        form, template_name, _ = get_form_and_template(requirement)

        return render(request, template_name, {
            'form': form,
            "request_changes_form": request_changes_form,
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


class NeedsAuthorisationView(View):
    template_name = 'needs_auth.html'

    def get(self, request, *args, **kwargs):
        requirement_id = self.kwargs['requirement_id']
        requirement = Requirement.objects.filter(
            uuid=requirement_id,
        ).first()

        if not requirement:
            raise Http404("Cannot find requirement")

        return render(request, self.template_name, {
            "current_state": REQUIREMENT_STATES[requirement.state]["nice_name"],
        })
