from django.shortcuts import render, reverse, redirect
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


class FlowCreateView(CreateView):
    model = Flow
    fields = ["workflow_name"]

    def get_success_url(self):
        return reverse("flow", args=[self.object.pk])


class FlowStartView(View):
    def post(self, request, pk, **kwargs):
        flow = Flow.objects.get(pk=pk)

        executor = WorkflowExecutor(flow)
        executor.run_flow(user=self.request.user)

        return redirect(reverse("flow", args=[flow.pk]))


class FlowContinueView(View):
    def get(self, request, pk, **kwargs):
        flow = Flow.objects.get(pk=pk)

        context = {}

        step = flow.workflow.get_step(flow.current_task_record.step_id)
        task = step.task
        context["step"] = step
        context["task"] = task
        context["flow"] = flow

        if not task.auto:
            context["form"] = task.form()

        return render(request, "workflow/flow-continue.html", context=context)

    def post(self, request, pk, **kwargs):
        flow = Flow.objects.get(pk=pk)

        task_uuid = self.request.POST["uuid"]
        executor = WorkflowExecutor(flow)
        executor.run_flow(
            user=self.request.user, task_info=self.request.POST, task_uuid=task_uuid
        )

        return redirect(reverse("flow", args=[flow.pk]))


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
