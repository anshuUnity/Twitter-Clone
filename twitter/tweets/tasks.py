from celery.decorators import task
from celery.utils.log import get_task_logger
from django.core.mail import EmailMessage
from time import sleep
logger = get_task_logger(__name__)

@task(name='my_first_task')
def my_first_task(duration):
    sleep(duration)
    return('first_task_done')

@task(name='send_email_task')
def send_mail_task(subject, message, email_from, recepient_list):
    msg = EmailMessage(subject, message, email_from, recepient_list)
    msg.content_subtype = 'html'
    msg.send()