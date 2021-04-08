from notifications_python_client.notifications import (
    NotificationsAPIClient,
)

from django.conf import settings


def send_email(to, template_id, personalisation={}):
    notification_client = NotificationsAPIClient(settings.GOVUK_NOTIFY_API_KEY)
    message_sent = notification_client.send_email_notification(
        email_address=to,
        template_id=template_id,
        personalisation=personalisation,
    )

    return message_sent
