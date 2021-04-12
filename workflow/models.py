import uuid

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.db import models
from django.urls import reverse

from django_fsm import FSMField, transition

from chartofaccount.models import (
    DepartmentalGroup,
    Directorate,
    CostCentre,
)

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


CHIEF_APPROVAL_REQUIRED = "chief_approval_required"
CHIEF_REQUESTS_CHANGES = "chief_requests_changes"

BUS_OPS_APPROVAL_REQUIRED = "bus_ops_approval_required"
IN_PROGRESS = "in_progress"
DIRECTOR_APPROVED = "director_approved"
DG_COO_APPROVED = "dg_coo_approved"
COMPLETE = "complete"

REQUIREMENT_STATES = {
    CHIEF_APPROVAL_REQUIRED: {
        "nice_name": "Chief approval required",
        "permissions": ["can_give_chief_approval", ]
    },
    CHIEF_REQUESTS_CHANGES: {
        "nice_name": "A chief has requested changes",
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


class AuditLog(models.Model):
    action_at = models.DateTimeField(auto_now_add=True)
    message = models.CharField(max_length=255)
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
    )
    requirement = models.ForeignKey(
        "Requirement",
        on_delete=models.CASCADE,
    )


class Comment(models.Model):
    submitted_at = models.DateTimeField(auto_now_add=True)
    message = models.CharField(max_length=255)
    parent = models.ForeignKey(
        "Comment",
        on_delete=models.CASCADE,
        null=True,
    )
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
    )
    requirement = models.ForeignKey(
        "Requirement",
        on_delete=models.CASCADE,
    )
    acted_on = models.BooleanField(
        default=False,
    )


class Requirement(models.Model):
    CONTRACTOR_TYPE_GENERALIST = 'generalist'
    CONTRACTOR_TYPE_SPECIALIST = 'specialist'
    CONTRACTOR_TYPE_CHOICES = [
        (CONTRACTOR_TYPE_GENERALIST, 'Generalist'),
        (CONTRACTOR_TYPE_SPECIALIST, 'Specialist'),
    ]
    SECURITY_CLEARANCE_BPSS = "BPSS"
    SECURITY_CLEARANCE_SC = "sc"
    SECURITY_CLEARANCE_DV = "dv"
    SECURITY_CLEARANCE_CTC = "ctc"
    SECURITY_CLEARANCE_CHOICES = [
        (SECURITY_CLEARANCE_BPSS , "BPSS"),
        (SECURITY_CLEARANCE_SC , "SC"),
        (SECURITY_CLEARANCE_DV , "DV"),
        (SECURITY_CLEARANCE_CTC , "CTC"),
    ]
    IR35_IN = 'in'
    IR35_OUT = 'out'
    IR35_CHOICES = [
        (IR35_IN, 'IN'),
        (IR35_OUT, 'OUT'),
    ]

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
    project_name_role_title = models.CharField(
        max_length=255,
        verbose_name="Project name/ Title of the Role"
    )
    IR35 = models.CharField(
        max_length=50,
        choices=IR35_CHOICES,
        verbose_name="IN / OUT of Scope of IR35"
    )
    new_requirement = models.BooleanField(verbose_name="New")
    name_of_contractor = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="If Nominated Worker - please provide Name of the contractor"
    )
    uk_based = models.BooleanField(default=True, verbose_name="UK based")
    overseas_country = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="if Overseas which Country"
    )
    start_date = models.DateField(verbose_name="Anticipated Start Date")
    end_date = models.DateField(verbose_name="Anticipated End Date")
    type_of_security_clearance = models.CharField(
        max_length=50,
        choices=SECURITY_CLEARANCE_CHOICES,
        verbose_name="Level of Security clearance required"
    )
    contractor_type = models.CharField(
        max_length=50,
        choices=CONTRACTOR_TYPE_CHOICES,
        verbose_name="Category of Interim"
    )
    part_b_business_case = models.TextField(
        verbose_name="Business Case: Please detail why the interim resource is required."
    )
    part_b_impact = models.TextField(
        verbose_name="What would be the impact of not filling this requirement."
    )
    part_b_main_reason = models.TextField(
        verbose_name="What are the main reasons why this role has not been filled by a substantive Civil Servant. Please detail the strategic workforce plan for this role after the assignment end date:"
    )
    job_description_submitted = models.BooleanField(default=False)

    directorate = models.ForeignKey(
        Directorate,
        on_delete=models.CASCADE,
        related_name="directorates",
    )

    state = FSMField(
        default=CHIEF_APPROVAL_REQUIRED,
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
    group = models.ForeignKey(
        DepartmentalGroup,
        on_delete=models.CASCADE,
        related_name="groups",
    )
    cost_centre_code = models.ForeignKey(
        CostCentre,
        on_delete=models.CASCADE,
        related_name="costcentres",
        verbose_name="Cost Centre/Team"
    )

    slot_codes = models.CharField(max_length=255)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Email chief
        if self.state == CHIEF_APPROVAL_REQUIRED:
            self.send_chiefs_email("A new hiring requirement has been submitted for approval")

        AuditLog.objects.create(
            user=self.hiring_manager,
            message="Requirement created, approval requested from a chief",
            requirement=self,
        )

    def send_chiefs_email(self, subject):
        chiefs_group = Group.objects.filter(
            name="Chiefs",
        ).first()

        chiefs = User.objects.filter(
            groups=chiefs_group,
        )

        for chief in chiefs:
            send_email(
                subject=subject,
                message=f"Please approve the hiring requirement at http://localhost:8000/approval/{self.uuid}/",
                to=chief.email,
                template_id=settings.CHIEF_APPROVAL_REQUEST_TEMPLATE_ID,
                personalisation={
                    "requirement_link": reverse(
                        "approval",
                        kwargs={
                            'requirement_id': self.uuid}
                    ),
                },
            )

    @property
    def nice_name(self):
        return REQUIREMENT_STATES[self.state]["nice_name"]

    @property
    def has_departmental_approval(self):
        if self.finance_approval and self.hr_approval and self.commercial_approval:
            return True

        return False

    @transition(field=state, source=CHIEF_APPROVAL_REQUIRED, target=BUS_OPS_APPROVAL_REQUIRED)
    def give_chief_approval(self):
        bus_ops_group = Group.objects.filter(
            name="Business Operations",
        ).first()

        bus_ops = User.objects.filter(
            groups=bus_ops_group,
        )

        for bus_op in bus_ops:
            send_email(
                subject="A hiring requirement is ready for your approval",
                message=f"Please see http://localhost:8000/requirement/{self.uuid}/",
                to=bus_op.email,
                template_id=settings.BUS_OPS_APPROVAL_REQUEST_TEMPLATE_ID,
                personalisation={
                    "requirement_link": reverse(
                        "approval",
                        kwargs={
                            'requirement_id': self.uuid}
                    ),
                },
            )

    @transition(field=state, source=CHIEF_APPROVAL_REQUIRED, target=CHIEF_REQUESTS_CHANGES)
    def request_changes_chief(self):
        send_email(
            subject="Changes have been requested to your hiring requirement",
            message=f"Please see http://localhost:8000/requirement/{self.uuid}/",
            to=self.hiring_manager.email,
            template_id=settings.HIRING_MANAGER_CHANGES_REQUESTED_TEMPLATE_ID,
            personalisation={
                "requirement_link": reverse(
                    "approval",
                    kwargs={
                        'requirement_id': self.uuid}
                ),
            },
        )

    @transition(field=state, source=CHIEF_REQUESTS_CHANGES, target=CHIEF_APPROVAL_REQUIRED)
    def made_changes_chief(self):
        self.send_chiefs_email(subject="A hiring requirement has been resubmitted for approval")

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
