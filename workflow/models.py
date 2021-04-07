import uuid

from django.contrib.auth import get_user_model
from django.db import models

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


class Requirement(models.Model):
    uuid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    submitter = models.ForeignKey(
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

    @property
    def has_departmental_approval(self):
        if self.finance_approval and self.hr_approval and self.commercial_approval:
            return True

        return False

    @transition(field=state, source='submitted', target='in_progress')
    def give_chief_approval(self):
        pass
        # Get group to send email to
        #send_email()

    @transition(field=state, source='in_progress', target='director_approved')
    def give_director_approval(self):
        pass

    @transition(field=state, source='director_approved', target='dg_coo_approved')
    def give_dg_coo_approval(self):
        pass

    @transition(field=state, source='dg_coo_approved', target='complete')
    def hiring_manager_approval(self):
        pass

    @transition(field=state, source='dg_coo_approved', target='reconsider')
    def hiring_manager_rejection(self):
        pass


class RequirementSubmitStep(models.Model):
    name_of_hiring_manager = models.CharField(max_length=255)
    requirement = models.ForeignKey(
        Requirement,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )


class RequirementFinanceStep(models.Model):
    cost_centre_code = models.CharField(max_length=255)
    requirement = models.ForeignKey(
        Requirement,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )


class RequirementHRStep(models.Model):
    slot_codes = models.CharField(max_length=255)
    requirement = models.ForeignKey(
        Requirement,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )


class RequirementCommercialStep(models.Model):
    professional_services_team = models.CharField(max_length=255)
    requirement = models.ForeignKey(
        Requirement,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )


class RequirementHiringManagerStep(models.Model):
    professional_services_team = models.CharField(max_length=255)
    requirement = models.ForeignKey(
        Requirement,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
