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
    AuditLog,
    Comment,
    Requirement,
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
            hiring_manager=self.request.user,
        )

        if self.request.user.has_perm(
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

        return requirements.order_by("-submitted_on")


class RequirementView(View):
    template_name = 'requirement.html'
    form_class = NewRequirementForm

    def dispatch(self, request, *args, **kwargs):
        requirement_id = self.kwargs['requirement_id']
        self.requirement = Requirement.objects.filter(
            uuid=requirement_id,
        ).first()

        if not self.requirement:
            raise Http404("Cannot find requirement")

        self.comments = Comment.objects.filter(
            requirement=self.requirement,
            acted_on=False,
        ).order_by("-submitted_at")

        self.audit_log = AuditLog.objects.filter(
            requirement=self.requirement,
        ).order_by("-action_at")

        return super(RequirementView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = self.form_class(instance=self.requirement)

        return render(request, self.template_name, {
            "form": form,
            "requirement": self.requirement,
            "comments": self.comments,
            "audit_log": self.audit_log,
        })

    def post(self, request, *args, **kwargs):
        form = self.form_class(
            request.POST,
            instance=self.requirement,
            hiring_manager=request.user
        )

        if form.is_valid():
            form.save()
            self.requirement.made_changes_chief()
            self.requirement.save()

            for comment in self.comments:
                comment.acted_on = True
                comment.save()

            return HttpResponseRedirect(
                reverse("requirements")
            )

        return render(request, self.template_name, {
            "form": form,
            "requirement": self.requirement,
            "comments": self.comments,
            "audit_log": self.audit_log,
        })


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
            form.save()
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
        template_name = "approval.html"
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
                    "requirement",
                    kwargs={"requirement_id": requirement_id}
                )
            )

        if not requirement:
            raise Http404("Cannot find requirement")

        form, template_name, _ = get_form_and_template(requirement)

        return render(request, template_name, {
            'form': form,
            "request_changes_form": RequestChangesForm(),
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
            "request_changes_form": RequestChangesForm(),
            'requirement': requirement,
        })


class ApprovedView(View):
    template_name = 'approved.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class UsersView(View):
    template_name = 'users.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class ProcessOwnerView(View):
    template_name = 'process_owner.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class RequestSubmittedView(View):
    template_name = 'changes_requested.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


# Request changes
class RequestChangesView(View):
    def get(self, request, *args, **kwargs):
        requirement_id = self.kwargs['requirement_id']
        requirement = Requirement.objects.filter(
            uuid=requirement_id,
        ).first()

        if not requirement:
            raise Http404("Cannot find requirement")

        form = RequestChangesForm()

        return render(request, self.template_name, {
            'form': form,
            'requirement': requirement,
        })

    def post(self, request, *args, **kwargs):
        requirement_id = self.kwargs['requirement_id']
        requirement = Requirement.objects.filter(
            uuid=requirement_id,
        ).first()

        if not requirement:
            raise Http404("Cannot find requirement")

        form = RequestChangesForm(request.POST)

        if form.is_valid():
            message = form.cleaned_data['message']

            Comment.objects.create(
                message=message,
                user=request.user,
                requirement=requirement,
            )

            requirement.request_changes_chief()
            requirement.save()

            AuditLog.objects.create(
                message="Changes were requested",
                user=request.user,
                requirement=requirement,
            )

            return HttpResponseRedirect(
                reverse("change_request_submitted")
            )

        return render(request, self.template_name, {
            'form': form,
            'requirement': requirement,
        })
