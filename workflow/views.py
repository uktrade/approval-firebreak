from django.shortcuts import render, reverse, redirect
from django.http import JsonResponse
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

        if not flow.current_task_record:
            return redirect(reverse("flow-list"))

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


class FlowDiagramView(View):
    def get(self, request, pk, **kwargs):
        flow = Flow.objects.get(pk=pk)

        elements = workflow_to_cytoscape_elements(flow)

        return JsonResponse({"elements": elements})


def workflow_to_cytoscape_elements(flow):
    nodes = [step_to_node(flow, step) for step in flow.workflow.steps]

    edges = []
    for step in flow.workflow.steps:
        targets = step.target if isinstance(step.target, list) else [step.target]
        for target in targets:
            if not target:
                continue

            edges.append(
                {
                    "data": {
                        "id": f"{step.step_id}{target}",
                        "source": step.step_id,
                        "target": target,
                    }
                }
            )

    return [*nodes, *edges]


def step_to_node(flow, step):
    latest_step_task = (
        flow.tasks.order_by("started_at").filter(step_id=step.step_id).last()
    )

    targets = []

    if step.target:
        targets = step.target if isinstance(step.target, list) else [step.target]

    end = not bool(targets)
    done = latest_step_task and bool(latest_step_task.finished_at)

    label = step.description or format_step_id(step.step_id)
    if end and done:
        label += " ✓"

    return {
        "data": {
            "id": step.step_id,
            "label": label,
            "start": step.start,
            "end": end,
            "decision": len(targets) > 1,
            "done": done,
            "current": latest_step_task and not latest_step_task.finished_at,
        }
    }


def format_step_id(step_id):
    # email_all_users -> Email all users
    return step_id.replace("_", " ").title()
