from django.conf import settings
from django.core.mail import EmailMessage
from core.models import *


def send_mail_check(name, subject_mail, subject_user, message, to, reply_to=settings.DEFAULT_FROM_EMAIL):
    success = True
    error_message = None

    try:
        email = EmailMessage(
            subject_mail,
            message,
            to=[to],
            reply_to=[reply_to]
        )
        email.send()
    except Exception as e:
        success = False
        error_message = str(e)

    Message.objects.create(
        name=name,
        subject=subject_user,
        email=to,
        message=message,
        error_message=error_message,
        success=success,
    )


def send_mail_both(name, subject_mail, subject_user, message, to, reply_to=settings.DEFAULT_FROM_EMAIL):
    from core.tasks import send_mail_queued

    # Mail to ADMIN
    # send_mail_check(
    #     name=name,
    #     subject_mail=subject_mail,
    #     subject_user=subject_user,
    #     message=message,
    #     to=settings.DEFAULT_FROM_EMAIL,
    #     reply_to=to,
    # )
    send_mail_queued.delay(
        mail_subject=subject_mail,
        message_context=message,
        to=settings.DEFAULT_FROM_EMAIL,
        reply_to=to,
    )

    # Mail to USER
    # send_mail_check(
    #     name=name,
    #     subject_mail=subject_mail,
    #     subject_user=subject_user,
    #     message=message,
    #     to=to,
    #     reply_to=reply_to,
    # )
    # REMOVED FOR TEMPORARY
    # send_mail_queued.delay(
    #     mail_subject=subject_mail,
    #     message_context=message,
    #     to=to,
    #     reply_to=reply_to,
    # )


def get_val_in_type(value, val_type):
    try:
        if val_type == 'str':
            value = str(value)
        elif val_type == 'int':
            value = int(value)
        elif val_type == 'float':
            value = float(value)
        elif val_type == 'bool':
            if str(value).lower() == 'true':
                value = True
            elif str(value).lower() == 'false':
                value = False
            elif str(value).lower() == 'none':
                value = None
            else:
                value = None
    except:
        value = None

    return value


def get_parameter(setting, val_type='str'):
    try:
        parameter = GeneralSetting.objects.get(name=setting).parameter
    except:
        parameter = ''

    parameter = get_val_in_type(parameter, val_type)

    return parameter


def get_image(setting):
    try:
        image = ImageSetting.objects.get(name=setting).file.url
        if not image:
            raise Exception
    except:
        image = settings.DEFAULT_PNG

    return image
