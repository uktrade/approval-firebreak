from django.utils import timezone

from workflow.models import TaskRecord


class WorkflowError(Exception):
    pass


class WorkflowExecutor:
    def __init__(self, flow):
        self.flow = flow

    def run_flow(self, user, task_info=None, task_uuid=None):
        if task_info is None:
            task_info = {}

        # TODO: might be a race condition
        if self.flow.started and not task_uuid:
            raise WorkflowError("Flow already started")

        self.flow.started = timezone.now()
        self.flow.save()

        if task_uuid:
            current_step = self.flow.workflow.get_step(
                TaskRecord.objects.get(uuid=task_uuid).step_id
            )
        else:
            current_step = self.flow.workflow.first_step

        while current_step:
            task_record, created = TaskRecord.objects.get_or_create(
                flow=self.flow,
                task_name=current_step.task_name,
                step_id=current_step.step_id,
                executed_by=None,
                defaults={"task_info": current_step.task_info or {}},
            )

            task = current_step.task(user, task_record, self.flow)

            task.setup(task_info)

            # the next task has a manual step
            if not task.auto and created:
                return task_record

            target, task_output = task.execute(task_info)

            # TODO: check target against step target

            task_record.finished_at = timezone.now()
            task_record.save()
            self.flow.save()

            current_step = next(
                (
                    step
                    for step in self.flow.workflow.steps
                    if step.step_id == (target or current_step.target)
                ),
                None,
            )

            task_info = task_output

        self.flow.finished = timezone.now()
        self.flow.save()

        return task_record
