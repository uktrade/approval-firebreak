from workflow.task import Task


class SendApproverEmail(Task, input="first_approval_given"):
    auto = False

    def execute(self, process):
        print("Executing send approver email...")

        # TODO - send approver email
        # Happy path
        output = "email_sent"

        return output
