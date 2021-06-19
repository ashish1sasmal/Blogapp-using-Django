from django.conf import settings
from django.core.mail import send_mail

def emailSend(subject, message, recipent_list):
    try:
        email_from = settings.EMAIL_HOST_USER
        recipient_list = recipent_list
        send_mail( subject, message, email_from, recipient_list )
        return True
    except Exception as e:
        print(e)
        return False
