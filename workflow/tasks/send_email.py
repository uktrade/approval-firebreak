from django.core.mail import send_mail

from .task import Task


class SendEmail(Task, input="send_email"):
    auto = True

    def execute(self, **kwargs):
        successfully_sent = send_mail(
            subject=kwargs.get("subject", self.task_record.task_info["subject"]),
            message=kwargs.get("message", self.task_record.task_info["message"]),
            from_email=kwargs.get(
                "from_email", self.task_record.task_info["from_email"]
            ),
            recipient_list=kwargs.get(
                "recipient_list", self.task_record.task_info["recipient_list"]
            ),
            fail_silently=False,
        )

        return None, {"successfully_sent": successfully_sent}
