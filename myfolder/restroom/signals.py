import pickle
# for encoding/decoding messages in base64
from base64 import urlsafe_b64encode
from datetime import datetime
# for dealing with attachement MIME types
from email.mime.text import MIMEText

from django.db.models.signals import post_save
from django.dispatch import receiver
# Gmail API utils
from googleapiclient.discovery import build

from .models import Alert_history, AlertConditions


def get_time_difference(time1, time2):
    time_difference = time1 - time2
    return time_difference.total_seconds() // 60


@receiver(post_save, sender=Alert_history)
def post_save_alerts(sender, instance, created, **kwargs):
    """
        Check the values and send alert email
    """
    if created:
        # get latest email history
        email_history = Alert_history.objects.filter(
            parameter=instance.parameter, is_email_sent=True).last()
        # Get Email address
        email_address = AlertConditions.objects.first().email
        # split email address
        email_address_list = email_address.split(",")

        if email_history is not None:
            time_difference = get_time_difference(
                datetime.now(), email_history.created_at)
            if time_difference > 30:
                for email in email_address_list:
                    mail_message = sent_mail(instance.parameter, instance.data, email)

                    # update is_email_sent to True for email history
                    if mail_message == "success":
                        Alert_history.objects.filter(id=instance.id).update(
                            is_email_sent=True
                        )
        else:
            for email in email_address_list:
                mail_message = sent_mail(instance.parameter, instance.data, email)
                # update is_email_sent to True to the instance
                if mail_message == "success":
                    instance.is_email_sent = True
                    instance.save()


def sent_mail(parameter, data, email):
    """
        Send email to the user
    """
    try:
        with open("creds/token.pickle", "rb") as token:
            creds = pickle.load(token)
        service = build("gmail", "v1", credentials=creds)
        message = MIMEText(f"Current {parameter} value is {data['value']} and it's {data['threshold']} threshold value.")
        message["to"] = email
        message["subject"] = "Alert from Building Monitoring System"

        service.users().messages().send(
            userId="me", body={"raw": urlsafe_b64encode(message.as_bytes()).decode()}
        ).execute()

        return "success"
    except Exception as e:
        print(e)
        return "error"