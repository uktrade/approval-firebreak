import uuid

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.db import models

from chartofaccount.models import (
    DepartmentalGroup,
    Directorate,
    CostCentre,
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
