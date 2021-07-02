from django.contrib.auth import get_user_model

from workflow.tasks import Task


class FindApproverRecipients(Task, input="find_approver_recipients"):
    auto = True

    def execute(self, task_info):
        User = get_user_model()
        users = User.objects.filter(
            groups__name=self.task_record.task_info["group_name"]
        )

        return None, {"recipient_list": list(users.values_list("email"))}
