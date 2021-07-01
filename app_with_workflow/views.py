from django.shortcuts import render
from django.utils import timezone
from django.views import View
from django.views.generic.edit import FormView, CreateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.http import JsonResponse

from app_with_workflow.forms import ApproveRequirementForm
from workflow.executor import WorkflowExecutor

from workflow.models import Flow


class FlowListView(ListView):
    model = Flow
    paginate_by = 100  # if pagination is desired


class FlowView(DetailView):
    model = Flow

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        flow = self.get_object()
        if flow.current_task_record:
            step = flow.workflow.get_step(flow.current_task_record.step_id)
            task = step.task
            context["step"] = step
            context["task"] = task

            if not task.auto:
                context["form"] = task.form()

        return context


class FlowCreateView(CreateView):
    model = Flow
    fields = ["workflow_name"]


class FlowStartView(View):
    def post(self, request, pk, **kwargs):
        flow = Flow.objects.get(pk=pk)

        executor = WorkflowExecutor(flow)
        executor.run_flow(user=self.request.user)

        return JsonResponse({"flow_id": flow.pk})


class FlowProceedView(View):
    def post(self, request, pk, **kwargs):
        flow = Flow.objects.get(pk=pk)

        task_uuid = self.request.POST["uuid"]
        executor = WorkflowExecutor(flow)
        executor.run_flow(
            user=self.request.user, task_info=self.request.POST, task_uuid=task_uuid
        )

        return JsonResponse({"flow_id": flow.pk})


# Starts process
class RequirementView(FormView):
    template_name = "requirement.html"
    form_class = ApproveRequirementForm

    def get(self, request, *args, **kwargs):
        form = self.form_class(instance=self.requirement)

        return render(
            request,
            self.template_name,
            {
                "form": form,
            },
        )

    def post(self, request, *args, **kwargs):
        form = self.form_class(
            request.POST,
            instance=self.requirement,
        )

        if form.is_valid():
            form.save()
            process = WorkflowExecutor.start_process()

        return render(
            request,
            self.template_name,
            {
                "form": form,
            },
        )
