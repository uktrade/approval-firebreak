from dataclasses import dataclass
from typing import Optional

from workflow.tasks import Task


@dataclass
class Step:
    step_id: str
    task_name: str
    target: Optional[str]
    start: Optional[bool] = None
    task_info: Optional[dict] = None

    @property
    def task(self):
        return Task.tasks[self.task_name]


@dataclass
class Workflow:
    name: str
    steps: list[Step]

    def get_step(self, step_id):
        return next(step for step in self.steps if step.step_id == step_id)

    @property
    def first_step(self):
        return next(step for step in self.steps if step.start)


ExampleWorkflow = Workflow(
    name="example_workflow",
    steps=[
        Step(
            step_id="send_first_email",
            task_name="send_email",
            start=True,
            target="send_second_email",
            task_info={
                "subject": "Test subject",
                "message": "Test message",
                "from_email": "admin@example.com",
                "recipient_list": ["approver@example.com"],
            },
        ),
        Step(
            step_id="send_second_email",
            task_name="send_email",
            target="send_third_email",
            task_info={
                "subject": "Test subject 2",
                "message": "Test message 2",
                "from_email": "admin2@example.com",
                "recipient_list": ["approver2@example.com"],
            },
        ),
        Step(
            step_id="send_third_email",
            task_name="send_email",
            target=None,
            task_info={
                "subject": "Test subject 3",
                "message": "Test message 3",
                "from_email": "admin3@example.com",
                "recipient_list": ["approver3@example.com"],
            },
        ),
    ],
)
