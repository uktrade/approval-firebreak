
class Task:
    tasks = {}

    def execute(self, task_input):
        raise NotImplementedError()

    def __init_subclass__(cls, /, input, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.tasks[input] = cls
