from workflow.models import Flow, TaskRecord
from workflow.task import Task


class WorkflowExecutor:
    @staticmethod
    def start_process():
        return Flow.objects.create()

    @staticmethod
    def execute_task(input, task_info, flow=None):
        if input == "start":
            flow = Flow.objects.create()
        elif flow is None:  # if input not start this should never happen
            raise ValueError()

        task = Task.tasks[input]()
        output, task_info = task.execute(flow=flow, )






        # Go to parent class and get
        # subclass with matching input
        # execute task class

        output = "executed task output"

        TaskRecord.objects.create(
            process=process,
            input=input,
            output=output,
        )

        # Check for next task having user involvement
        # if it doesn't execute it
        # if not task.user_actioned:
        self.execute_task(input=output, process=process)
