from django.utils import timezone

from workflow.models import Flow, TaskRecord
from workflow.task import Task


class WorkflowExecutor:
    @staticmethod
    def start_process():
        return Flow.objects.create()

    @classmethod
    def resume(cls, task_record_uuid, task_info: dict = None):
        task_record = TaskRecord.objects.get(uuid=task_record_uuid)

        cls.execute_task(
            input=task_record.input,
            task_info=task_info,
            flow=task_record.flow,
            user=task_record.user,
        )

    @classmethod
    def execute_task(cls, input: str, task_info: dict = None, flow=None, user=None):
        if input == "start":
            flow = Flow.objects.create()
        elif input == "end":
            flow.finished = timezone.now()
            flow.save()
            return
        elif flow is None:  # if input not start this should never happen
            raise ValueError("flow cannot be None")

        task_cls = Task.tasks[input]

        task_record, created = TaskRecord.objects.get_or_create(
            flow=flow,
            executed_by=user,
            input=input,
            defaults={"task_info": task_info},
        )

        task = task_cls(task_record, flow)

        task.setup(**task_info)

        # the next task has a manual step
        if not task.auto and created:
            return task_record

        output, output_task_info = task.execute(
            flow=flow, task_record=task_record, **task_info
        )

        task_record.finished_at = timezone.now()
        task_record.output = output
        task_record.save()

        cls.execute_task(input=output, task_info=output_task_info, flow=flow, user=user)

        return task_record
