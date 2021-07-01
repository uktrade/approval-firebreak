from django.shortcuts import render
from django.utils import timezone
from django.views import View
from django.views.generic.edit import FormView
from django.views.generic.list import ListView

from app_with_workflow.forms import ApproveRequirementForm
from workflow.executor import WorkflowExecutor

from app_with_workflow.models import Requirement


class RequirementsView(ListView):
    model = Requirement
    paginate_by = 100  # if pagination is desired

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context


# Starts process
class RequirementView(FormView):
    template_name = 'requirement.html'
    form_class = ApproveRequirementForm

    def get(self, request, *args, **kwargs):
        form = self.form_class(instance=self.requirement)

        return render(request, self.template_name, {
            "form": form,
        })

    def post(self, request, *args, **kwargs):
        form = self.form_class(
            request.POST,
            instance=self.requirement,
        )

        if form.is_valid():
            form.save()
            process = WorkflowExecutor.start_process()

        return render(request, self.template_name, {
            "form": form,
        })
