from notifications_python_client.notifications import (
    NotificationsAPIClient,
)

from django.conf import settings

from django.core.mail import send_mail


def send_email(subject, message, to, template_id, personalisation={}):
    send_mail(
        subject,
        message,
        'from@approval-firebreak.com',
        [to],
        fail_silently=False,
    )


# def send_email(to, template_id, personalisation={}):
#     notification_client = NotificationsAPIClient(settings.GOVUK_NOTIFY_API_KEY)
#
#     try:
#         message_sent = notification_client.send_email_notification(
#             email_address=to,
#             template_id=template_id,
#             personalisation=personalisation,
#         )
#
#         return message_sent
#     except Exception as ex:
#         print(ex)
