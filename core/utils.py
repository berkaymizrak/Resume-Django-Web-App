from core.enums import Browsers, Platforms
from django.conf import settings
from django.core.mail import EmailMessage
import traceback


def send_mail_check(name, subject_mail, subject_user, message, to, reply_to=settings.DEFAULT_FROM_EMAIL):
    from core.models import Message
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
    from core.models import GeneralSetting
    try:
        parameter = GeneralSetting.objects.get(name=setting).parameter
    except:
        parameter = ''
    parameter = get_val_in_type(parameter, val_type)

    return parameter


def get_image(setting):
    from core.models import ImageSetting
    try:
        image = ImageSetting.objects.get(name=setting).file.url
        if not image:
            raise Exception
    except:
        image = settings.DEFAULT_PNG

    return image


def delete_media_file(model, instance=None, delete_older=False, path=None):
    """
    Delete old file from media storage when new file is uploaded.
    If path is not None, delete file from path. If path is None, delete file from media storage and instance must be given.
    :param model: Django Model to connect related database row.
    :param instance: Instance of model that is currently uploaded.
    :param delete_older: If True, delete old file from media storage; if False, delete current object's file.
    :param path: Path of file. Optional.
    :return True if file is deleted, False if file is not deleted.:
    """

    # This setting can be added:
    # if settings.DEBUG:
    #     return False

    if path:
        old_file_path = path
    else:
        if not instance:
            return False
        if delete_older:
            # This is for updating instance process.
            # Delete older file that is on the instance.
            if not instance.pk:
                # Given instance is not saved yet. So there is no older file.
                return False

            try:
                instance_object = model.objects.get(pk=instance.pk)
            except model.DoesNotExist:
                # Given instance could not be found in database.
                return False
            new_file = instance.file
            try:
                new_file.file  # This will raise FileDoesNotExist if file is cleared from instance, which is file deletion request.
                if new_file._committed:
                    # New file is already uploaded.
                    # That case only possible when updating instance without changing file, which means old_file=new_file.
                    # Since they are equal, it must not be deleted. There is no actually new file.
                    old_file = None
                else:
                    # New file is not uploaded yet which means there is old file.
                    old_file = instance_object.file
            except:
                old_file = instance_object.file
        else:
            # Delete current file
            old_file = instance.file

        if old_file:
            old_file_path = old_file.name
        else:
            old_file_path = None

    if old_file_path:
        if instance.file.storage.exists(old_file_path):
            instance.file.storage.delete(old_file_path)
            return True

    return False


def get_first_object_or_none(queryset, *args, **kwargs):
    try:
        return queryset.get(*args, **kwargs)
    except queryset.model.MultipleObjectsReturned:
        return queryset.filter(*args, **kwargs).first()
    except queryset.model.DoesNotExist:
        return queryset.none()


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def get_user_agent(request):
    return request.META.get('HTTP_USER_AGENT', '')


def get_platform(request):
    for platform in Platforms.choices:
        if platform[0] in get_user_agent(request).lower():
            return platform[0]
    return Platforms.OTHER


def get_browser(request):
    for browser in Browsers.choices:
        if browser[0] in get_user_agent(request).lower():
            return browser[0]
    return Browsers.OTHER


def create_action_log(request, action, message='', success=True, data=None):
    from core.models import ActionLog
    get_params = request.GET.dict() if request.GET else {}
    try:
        ActionLog.objects.create(
            user=request.user if request.user.is_authenticated else None,
            action=action,
            message=message,
            method=request.method,
            success=success,
            data=data,
            get_params=get_params,
            platform=get_platform(request),
            browser=get_browser(request),
            ip_address=get_client_ip(request),
            user_agent=get_user_agent(request)[0:255],
        )
    except:
        ActionLog.objects.create(
            user=request.user if request.user.is_authenticated else None,
            action=f'ERROR: {action}',
            message=str(traceback.format_exc()) + '\n\n' + str(message),
            method=request.method,
            success=success,
            data=None,
            get_params=None,
            platform=get_platform(request),
            browser=get_browser(request),
            ip_address=get_client_ip(request),
            user_agent=get_user_agent(request)[0:255],
        )
