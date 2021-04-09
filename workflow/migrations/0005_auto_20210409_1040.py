# Generated by Django 3.2 on 2021-04-09 09:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('workflow', '0002_rename_submitter_requirement_hiring_manager'),
    ]

    operations = [
        migrations.AddField(
            model_name='requirementsubmitstep',
            name='IR35',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='requirementsubmitstep',
            name='authorising_director',
            field=models.CharField(max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='requirementsubmitstep',
            name='contractor_type',
            field=models.CharField(choices=[('generalist', 'generalist'), ('specialist', 'specialist')],  max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='requirementsubmitstep',
            name='directorate',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='directorates', to='workflow.requirement'),
        ),
        migrations.AddField(
            model_name='requirementsubmitstep',
            name='email_of_authorising_director',
            field=models.EmailField(max_length=254),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='requirementsubmitstep',
            name='end_date',
            field=models.DateField(),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='requirementsubmitstep',
            name='job_description_submitted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='requirementsubmitstep',
            name='name_of_contractor',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='requirementsubmitstep',
            name='new_requirement',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='requirementsubmitstep',
            name='overseas_country',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='requirementsubmitstep',
            name='part_b_business_case',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='requirementsubmitstep',
            name='part_b_impact',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='requirementsubmitstep',
            name='part_b_main_reason',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='requirementsubmitstep',
            name='project_name_role_title',
            field=models.CharField( max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='requirementsubmitstep',
            name='start_date',
            field=models.DateField(),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='requirementsubmitstep',
            name='type_of_security_clearance',
            field=models.CharField(choices=[('BPSS', 'BPSS'), ('sc', 'sc'), ('dv', 'dv'), ('ctc', 'ctc')],  max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='requirementsubmitstep',
            name='uk_based',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='requirementsubmitstep',
            name='requirement',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='requirements', to='workflow.requirement'),
        ),
    ]
