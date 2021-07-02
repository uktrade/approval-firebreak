from django.shortcuts import render, reverse, redirect
from django.views import View
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from workflow.executor import WorkflowExecutor
from workflow.models import Flow


class FlowListView(ListView):
    model = Flow
    paginate_by = 100  # if pagination is desired
    ordering = "-started"


class FlowView(DetailView):
    model = Flow


class FlowCreateView(CreateView):
    model = Flow
    fields = ["workflow_name", "flow_name"]

    def get_success_url(self):
        return reverse("flow", args=[self.object.pk])

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.executed_by = self.request.user

        response = super().form_valid(form)

        executor = WorkflowExecutor(self.object)
        executor.run_flow(user=self.request.user)

        return response


class FlowContinueView(View):
    def get(self, request, pk, **kwargs):
        flow = Flow.objects.get(pk=pk)

        context = {}

        step = flow.workflow.get_step(flow.current_task_record.step_id)
        task = step.task(self.request.user, flow.current_task_record, flow)
        context["step"] = step
        context["task"] = task
        context["flow"] = flow

        if not task.auto:
            context |= task.context()

        template = task.template or "workflow/flow-continue.html"

        return render(request, template, context=context)

    def post(self, request, pk, **kwargs):
        flow = Flow.objects.get(pk=pk)

        task_uuid = self.request.POST["uuid"]
        executor = WorkflowExecutor(flow)
        executor.run_flow(
            user=self.request.user, task_info=self.request.POST, task_uuid=task_uuid
        )

        return redirect(reverse("flow", args=[flow.pk]))