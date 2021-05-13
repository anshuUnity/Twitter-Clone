from celery.decorators import task
from celery.utils.log import get_task_logger
from django.core.mail import EmailMessage
from time import sleep
logger = get_task_logger(__name__)

@task(name='send_email_otp_task')
def send_mail_otp_task(subject, message, email_from, recepient_list):
    msg = EmailMessage(subject, message, email_from, recepient_list)
    msg.content_subtype = 'html'
    msg.send()