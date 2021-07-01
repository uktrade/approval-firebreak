from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.db import models


class Flow(models.Model):
    workflow_name = ""  # app name
    created = models.DateTimeField(auto_now_add=True)


class TaskRecord(models.Model):
    started_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField()
    executed_by = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    flow = models.ForeignKey(
        Flow,
        on_delete=models.CASCADE,
        related_name="tasks"
    )
    input = models.CharField(max_length=100)
    output = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )


class TaskLog(models.Model):
    logged_at = models.DateTimeField()
    message = models.CharField(max_length=255)
    task_record = models.ForeignKey(
        TaskRecord,
        related_name="log",
        on_delete=models.CASCADE,
    )
