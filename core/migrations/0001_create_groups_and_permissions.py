from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.db import migrations

from workflow.models import Requirement


def create_groups_and_permissions(apps, schema_editor):
    content_type = ContentType.objects.get_for_model(Requirement)

    hiring_managers, _ = Group.objects.get_or_create(
        name="Hiring Managers",
    )
    hiring_managers.permissions.add(Permission.objects.create(
        codename='can_give_hiring_manager_approval',
        name='Can give hiring manager approval',
        content_type=content_type,
    ))

    chiefs, _ = Group.objects.get_or_create(
        name="Chiefs",
    )
    chiefs.permissions.add(Permission.objects.create(
        codename='can_give_chief_approval',
        name='Can give chief approval',
        content_type=content_type,
    ))

    bus_ops, _ = Group.objects.get_or_create(
        name="Business Operations",
    )
    bus_ops.permissions.add(Permission.objects.create(
        codename='can_give_bus_ops_approval',
        name='Can give business operations approval',
        content_type=content_type,
    ))

    commercial, _ = Group.objects.get_or_create(
        name="Commercial",
    )
    commercial.permissions.add(Permission.objects.create(
        codename='can_give_commercial_approval',
        name='Can give commercial approval',
        content_type=content_type,
    ))

    finance, _ = Group.objects.get_or_create(
        name="Finance",
    )
    finance.permissions.add(Permission.objects.create(
        codename='can_give_finance_approval',
        name='Can give finance approval',
        content_type=content_type,
    ))

    hr, _ = Group.objects.get_or_create(
        name="HR",
    )
    hr.permissions.add(Permission.objects.create(
        codename='can_give_hr_approval',
        name='Can give HR approval',
        content_type=content_type,
    ))

    ddat_director, _ = Group.objects.get_or_create(
        name="DDAT Director",
    )
    ddat_director.permissions.add(Permission.objects.create(
        codename='can_give_director_approval',
        name='Can give DDAT Director approval',
        content_type=content_type,
    ))
    dg_coo, _ = Group.objects.get_or_create(
        name="DG COO",
    )
    dg_coo.permissions.add(Permission.objects.create(
        codename='can_give_dg_coo_approval',
        name='Can give DG COO approval',
        content_type=content_type,
    ))


class Migration(migrations.Migration):

    dependencies = [("workflow", "0001_initial")]

    operations = [
        migrations.RunPython(create_groups_and_permissions),
    ]
