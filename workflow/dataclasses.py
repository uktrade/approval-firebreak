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
    description: Optional[str] = None

    @property
    def task(self):
        return Task.tasks[self.task_name]


@dataclass
class Workflow:
    name: str
    steps: list[Step]

    def get_step(self, step_id):
        return next((step for step in self.steps if step.step_id == step_id), None)

    @property
    def first_step(self):
        return next(step for step in self.steps if step.start)
