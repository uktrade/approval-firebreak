from workflow.task import Task


class InitialContractApproval(Task):
    input = "start"
    auto = False

    def execute(self, flow, **kwargs):
        print("Initial approval given...")

        # Happy path
        output = "initially_approved"

        return output, {}
