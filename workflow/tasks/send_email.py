from django.core.mail import send_mail

from .task import Task


class SendEmail(Task, input="send_email"):
    auto = True

    def execute(self, task_info):
        email_info = self.task_record.task_info | task_info

        successfully_sent = send_mail(
            **email_info,
            fail_silently=False,
        )

        return None, {"successfully_sent": successfully_sent}
