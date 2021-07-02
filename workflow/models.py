import uuid

from django.contrib.auth import get_user_model
from django.db import models

from app_with_workflow.workflow.approval_workflow import ApprovalWorkflow
from workflow.workflows.example import ExampleWorkflow


# TODO: make this more user friendly
WORKFLOW_NAME_WORKFLOW = {
    "example_workflow": ExampleWorkflow,
    "approval_workflow": ApprovalWorkflow,
}


class Flow(models.Model):
    WORKFLOWS = [
        ("example_workflow", "Example workflow"),
        ("approval_workflow", "Approval workflow"),
    ]

    workflow_name = models.CharField(choices=WORKFLOWS, max_length=255)
    started = models.DateTimeField(null=True)
    finished = models.DateTimeField(null=True, blank=True)

    @property
    def is_complete(self):
        return bool(self.finished)

    @property
    def workflow(self):
        return WORKFLOW_NAME_WORKFLOW[self.workflow_name]

    @property
    def current_task_record(self):
        return self.tasks.filter(finished_at__isnull=True).first()


class TaskRecord(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    started_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(null=True)
    executed_by = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    flow = models.ForeignKey(Flow, on_delete=models.CASCADE, related_name="tasks")
    step_id = models.CharField(max_length=100)
    task_name = models.CharField(max_length=100)
    target = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )
    task_info = models.JSONField(null=True, blank=True)

    def __str__(self):
        return f"{self.step_id} {self.task_name}"


class TaskLog(models.Model):
    logged_at = models.DateTimeField(auto_now_add=True)
    message = models.CharField(max_length=255)
    task_record = models.ForeignKey(
        TaskRecord,
        related_name="log",
        on_delete=models.CASCADE,
    )
