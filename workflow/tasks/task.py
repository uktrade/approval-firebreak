class Task:
    tasks = {}

    def __init__(self, task_record, flow):
        self.task_record = task_record
        self.flow = flow

    def setup(self, **kwargs):
        pass

    def execute(self, **kwargs):
        raise NotImplementedError

    def log(self, message):
        self.task_record.log.create(message=message)

    def __init_subclass__(cls, /, input, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.tasks[input] = cls
