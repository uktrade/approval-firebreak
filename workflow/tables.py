import django_tables2 as tables

from workflow.models import Requirement


class RequirementTable(tables.Table):
    class Meta:
        model = Requirement
        template_name = "django_tables_2_bootstrap.html"
