# user/tasks.py
from celery import shared_task
from user.celery import app

from django.conf import settings
from mailqueue.models import MailerMessage


@shared_task
def send_mail_queued(mail_subject, message_context, to, from_mail=settings.DEFAULT_FROM_EMAIL,
                     reply_to=None, cc=None, bcc=None, ):
    msg = MailerMessage()
    msg.subject = mail_subject
    msg.to_address = to

    # For sender names to be displayed correctly on mail clients, simply put your name first
    # and the actual email in angle brackets
    # Example correct sender value "Dave Johnston <dave@example.com>"
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
    msg.app = "Berkay MIZRAK Resume Web Project"

    msg.save()


from django.core.management import call_command


@shared_task
def command_send_queued_messages():
    # The management command for sending queued messages.
    # Command comes with mailqueue package.
    call_command('send_queued_messages')


@shared_task
def command_clear_sent_messages():
    # The management command for clearing sent messages from MailerMessage model of mailqueue package.
    # Command comes with mailqueue package.
    call_command('clear_sent_messages')


@shared_task
def command_clear_expired_sessions():
    # The management command for clearing expired sessions from Session model of django.contrib.sessions package.
    # This is a built-in management command of Django.
    # Suggested to use frequently to clear expired sessions based on number of guests you have.
    call_command('clearsessions')


import requests


@shared_task
def requests_send_queued_messages():
    # mailqueue package suggest to create an endpoint for triggering sending queued messages if you don't want to use it in regular way.
    url = 'https://berkaymizrak.com/mail-queue/'
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.108 Safari/537.36'
    headers = {
        'User-Agent': user_agent,
    }
    response = requests.get(url, headers=headers)


from django.contrib.admin.models import LogEntry


@shared_task
def clear_admin_logs(leave_last=100):
    # The management command for clearing admin logs from LogEntry model of django.contrib.admin package.
    # leave_last is the number of the latest logs to keep.
    model_say = LogEntry.objects.count()
    if model_say > leave_last:
        rows = LogEntry.objects.all()[:leave_last].values_list("id", flat=True)  # only retrieve ids.
        LogEntry.objects.exclude(pk__in=list(rows)).delete()


from user.models import ExpenseLog, PaymentLog, ActivityLog


@shared_task
def clear_model_logs(model='', leave_last=100):
    # The management command for clearing entries from a model that is given as a parameter.
    # leave_last is the number of the latest entries to keep.
    if model == 'Expense':
        Model = ExpenseLog
    elif model == 'Payment':
        Model = PaymentLog
    elif model == 'Activity':
        Model = ActivityLog
    else:
        return
    if Model.objects.count() > leave_last:
        rows = Model.objects.all()[:leave_last].values_list("id", flat=True)  # only retrieve ids.
        Model.objects.exclude(pk__in=list(rows)).delete()


from datetime import datetime
from user.models import Payment


@shared_task
def clear_expired_payments():
    # This is a logic to clear expired payments.
    now = datetime.now()
    query = Payment.objects.filter(valid_to__lt=now, payment_success=None, confirmation_success=None)
    query.delete()
