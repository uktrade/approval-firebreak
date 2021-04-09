import uuid

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse

from django_fsm import FSMField, transition

from core.notify import send_email


User = get_user_model()


class Approval(models.Model):
    FINANCE_APPROVED = 'fin_approved'
    HR_APPROVED = 'hr_approved'
    COMMERCIAL_APPROVED = 'comm_approved'
    APPROVAL_CHOICES = [
        (FINANCE_APPROVED, 'Finance has approved'),
        (HR_APPROVED, 'HR has approved'),
        (COMMERCIAL_APPROVED, 'Commercial has approved'),
    ]
    approved_at = models.DateTimeField(
        auto_now_add=True,
    )
    approver = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
    )
    approval_type = models.CharField(
        max_length=14,
        choices=APPROVAL_CHOICES,
    )

SUBMITTED = "submitted"
CHIEF_APPROVAL_REQUIRED = "chief_approval_required"
BUS_OPS_APPROVAL_REQUIRED = "bus_ops_approval_required"
IN_PROGRESS = "in_progress"
DIRECTOR_APPROVED = "director_approved"
DG_COO_APPROVED = "dg_coo_approved"
COMPLETE = "complete"

REQUIREMENT_STATES = {
    SUBMITTED: {
        "nice_name": "Submitted",
        "permissions": ["can_give_hiring_manager_approval", ]
    },
    CHIEF_APPROVAL_REQUIRED: {
        "nice_name": "Chief approval required",
        "permissions": ["can_give_chief_approval", ]
    },
    BUS_OPS_APPROVAL_REQUIRED: {
        "nice_name": "Business Operation approval required",
        "permissions": ["can_give_bus_ops_approval", ]
    },
    IN_PROGRESS: {
        "nice_name": "In progress",
        "permissions": [
            "can_give_commercial_approval",
            "can_give_finance_approval",
            "can_give_hr_approval",
        ]
    },
    DIRECTOR_APPROVED: {
        "nice_name": "Needs DO COO approval",
        "permissions": [
            "can_give_director_approval",
        ]
    },
    DG_COO_APPROVED: {
        "nice_name": "Needs hiring manager approval",
        "permissions": [
            "can_give_director_approval",
        ]
    },
}


class Requirement(models.Model):
    uuid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    hiring_manager = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
    )
    submitted_on = models.DateTimeField(
        auto_now_add=True,
    )
    state = FSMField(
        default='submitted',
    )
    finance_approval = models.ForeignKey(
        Approval,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="finance_approvals",
    )
    hr_approval = models.ForeignKey(
        Approval,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="hr_approvals",
    )
    commercial_approval = models.ForeignKey(
        Approval,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="commercial_approvals",
    )
    project_name_title_of_role = models.CharField(max_length=255)
    cost_centre_code = models.CharField(max_length=255)
    name_of_chief = models.CharField(max_length=255)
    email_of_chief = models.EmailField()
    slot_codes = models.CharField(max_length=255)

    @property
    def nice_name(self):
        return REQUIREMENT_STATES[self.state]["nice_name"]

    @property
    def has_departmental_approval(self):
        if self.finance_approval and self.hr_approval and self.commercial_approval:
            return True

        return False

    @transition(field=state, source=SUBMITTED, target=CHIEF_APPROVAL_REQUIRED)
    def give_hiring_manager_approval(self, chief_email):
        # Email Hiring manager
        send_email(
            to=chief_email,
            template_id=settings.CHIEF_APPROVAL_REQUEST_TEMPLATE_ID,
            personalisation={
                "requirement_link": reverse("approval", kwargs={'requirement_id': self.uuid}),
            },
        )



    @transition(field=state, source=CHIEF_APPROVAL_REQUIRED, target=BUS_OPS_APPROVAL_REQUIRED)
    def give_chief_approval(self):
        pass
        # Get group to send email to
        #send_email()


    @transition(field=state, source=BUS_OPS_APPROVAL_REQUIRED, target=IN_PROGRESS)
    def give_busops_approval(self):
        pass

    @transition(field=state, source=IN_PROGRESS, target=DIRECTOR_APPROVED)
    def give_director_approval(self):
        pass

    @transition(field=state, source=DIRECTOR_APPROVED, target=DG_COO_APPROVED)
    def give_dg_coo_approval(self):
        pass

    @transition(field=state, source=DG_COO_APPROVED, target=COMPLETE)
    def hiring_manager_approval(self):
        pass

    @transition(field=state, source=DG_COO_APPROVED, target='reconsider')
    def hiring_manager_rejection(self):
        pass
