from notifications_python_client.notifications import (
    NotificationsAPIClient,
)

from django.conf import settings


#
# personalisation = {
#                       "user_name": request.user.get_full_name(),
#                       "user_email": request.user.email,
#                       "page_url": last_viewed,
#                       "trying_to": trying_to,
#                       "what_went_wrong": what_went_wrong,
#                   },

def send_email(to, template_id, personalisation):
    notification_client = NotificationsAPIClient(settings.GOVUK_NOTIFY_API_KEY)
    message_sent = notification_client.send_email_notification(
        email_address=to,
        template_id=template_id,
        personalisation=personalisation,
    )

    return message_sent
