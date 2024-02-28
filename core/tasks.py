from celery import shared_task
from core.models import Message
from datetime import datetime
from django.apps import apps
from django.conf import settings
from django.core.management import call_command
from django.contrib.admin.models import LogEntry
from mailqueue.models import MailerMessage
from resume.celery import app
import requests


@shared_task
def send_mail_queued(mail_subject, message_context, to, from_mail=settings.DEFAULT_FROM_EMAIL,
                     reply_to=None, cc=None, bcc=None, ):
    msg = MailerMessage()
    msg.subject = mail_subject
    msg.to_address = to

    # For sender names to be displayed correctly on mail clients, simply put your name first
    # and the actual email in angle brackets
    # Example correct sender value 'Dave Johnston <dave@example.com>'
    msg.from_address = from_mail

    # As this is only an example, we place the text content in both the plaintext version (content)
    # and HTML version (html_content).
    msg.content = message_context
    message_html = message_context.replace('\n', '<br>')
    msg.html_content = message_html

    if cc:
        msg.cc_address = cc
    if bcc:
        msg.bcc_address = bcc
    if reply_to:
        msg.reply_to = reply_to

    # Name of your App that is sending the email.
    msg.app = 'Berkay MIZRAK'

    msg.save()


@shared_task
def command_clear_expired_sessions():
    # The management command for clearing expired sessions from Session model of django.contrib.sessions package.
    # This is a built-in management command of Django.
    # Suggested to use frequently to clear expired sessions based on number of guests you have.
    call_command('clearsessions')


@shared_task
def command_send_queued_messages():
    # The management command for sending queued messages.
    # Command comes with mailqueue package.
    call_command('send_queued_messages')


@shared_task
def requests_send_queued_messages():
    # mailqueue package suggest to create an endpoint for triggering sending queued messages
    # if you don't want to use it in regular way. (regular way: command_send_queued_messages)
    url = 'https://berkaymizrak.com/mail-queue/'
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.108 Safari/537.36'
    headers = {
        'User-Agent': user_agent,
    }
    response = requests.get(url, headers=headers)


@shared_task
def command_clear_sent_messages():
    # The management command for clearing sent messages from MailerMessage model of mailqueue package.
    # Command comes with mailqueue package.
    call_command('clear_sent_messages')


@shared_task
def clear_model_logs(app_label, model_name, leave_last=100):
    # The management command for clearing entries from a model that is given as a parameter.
    # leave_last is the number of the latest entries to keep.
    """
        # Set Arguments as:
        {
        "app_label" : "core",
        "model_name" : "message",
        "leave_last" : 100
        }
        # For admin logs:
        {
        "app_label" : "admin",
        "model_name" : "logentry",
        "leave_last" : 100
        }
    """
    print(f'[clear_model_logs] STARTED! app_label: {app_label}, model_name: {model_name}, leave_last: {leave_last}')
    try:
        MODEL = apps.get_model(app_label=app_label, model_name=model_name)
        leave_last = int(leave_last)
        if MODEL.objects.count() > leave_last:
            rows = MODEL.objects.all()[:leave_last].values_list('id', flat=True)  # only retrieve ids.
            MODEL.objects.exclude(pk__in=list(rows)).delete()
        print(f'[clear_model_logs] FINISHED! '
              f'app_label: {app_label}, model_name: {model_name}, leave_last: {leave_last}')
    except Exception as e:
        print(f'[clear_model_logs] Error on deletion: {e}')


@shared_task
def clear_expired_payments():
    # This is an example task to clear expired payments.
    # Not applicable for this project.
    now = datetime.now()
    query = Payment.objects.filter(valid_to__lt=now, payment_success=None, confirmation_success=None)
    query.delete()
