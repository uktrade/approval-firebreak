# Generated by Django 3.2 on 2021-04-12 10:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_fsm
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('chartofaccount', '0002_data'),
    ]

    operations = [
        migrations.CreateModel(
            name='Approval',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('approved_at', models.DateTimeField(auto_now_add=True)),
                ('approval_type', models.CharField(choices=[('fin_approved', 'Finance has approved'), ('hr_approved', 'HR has approved'), ('comm_approved', 'Commercial has approved')], max_length=14)),
                ('approver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Requirement',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('submitted_on', models.DateTimeField(auto_now_add=True)),
                ('project_name_role_title', models.CharField(max_length=255, verbose_name='Project name/ Title of the Role')),
                ('IR35', models.CharField(choices=[('in', 'IN'), ('out', 'OUT')], max_length=50, verbose_name='IN / OUT of Scope of IR35')),
                ('new_requirement', models.BooleanField(verbose_name='New')),
                ('name_of_contractor', models.CharField(blank=True, max_length=255, null=True, verbose_name='If Nominated Worker - please provide Name of the contractor')),
                ('uk_based', models.BooleanField(default=True)),
                ('overseas_country', models.CharField(blank=True, max_length=255, null=True, verbose_name='if Overseas which Country')),
                ('start_date', models.DateField(verbose_name='Anticipated Start Date')),
                ('end_date', models.DateField(verbose_name='Anticipated End Date')),
                ('type_of_security_clearance', models.CharField(choices=[('BPSS', 'BPSS'), ('sc', 'SC'), ('dv', 'DV'), ('ctc', 'CTC')], max_length=50, verbose_name='Level of Security clearance required')),
                ('contractor_type', models.CharField(choices=[('generalist', 'Generalist'), ('specialist', 'Specialist')], max_length=50, verbose_name='Category of Interim')),
                ('part_b_business_case', models.TextField(verbose_name='Business Case: Please detail why the interim resource is required.')),
                ('part_b_impact', models.TextField(verbose_name='What would be the impact of not filling this requirement.')),
                ('part_b_main_reason', models.TextField(verbose_name='What are the main reasons why this role has not been filled by a substantive Civil Servant. Please detail the strategic workforce plan for this role after the assignment end date:')),
                ('job_description_submitted', models.BooleanField(default=False)),
                ('state', django_fsm.FSMField(default='chief_approval_required', max_length=50)),
                ('project_name_title_of_role', models.CharField(max_length=255)),
                ('slot_codes', models.CharField(max_length=255)),
                ('commercial_approval', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='commercial_approvals', to='workflow.approval')),
                ('cost_centre_code', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='costcentres', to='chartofaccount.costcentre', verbose_name='Cost Centre/Team')),
                ('directorate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='directorates', to='chartofaccount.directorate')),
                ('finance_approval', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='finance_approvals', to='workflow.approval')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='groups', to='chartofaccount.departmentalgroup')),
                ('hiring_manager', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('hr_approval', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='hr_approvals', to='workflow.approval')),
            ],
        ),
        migrations.CreateModel(
            name='AuditLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action_at', models.DateTimeField(auto_now_add=True)),
                ('message', models.CharField(max_length=255)),
                ('requirement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='workflow.requirement')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
