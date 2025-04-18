from core.enums import Browsers, Platforms
from core.models import ActionLog, BlockedUser
from django.conf import settings
from django.core.mail import EmailMessage
import traceback
from django import forms
from django.core.serializers.json import DjangoJSONEncoder
from django.conf import settings
from django.contrib import messages
from django.db.models import Model, Q
from django.utils.safestring import mark_safe
from django.utils.html import strip_tags
from django.utils.translation import get_language
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
import random
import string
import traceback
import requests
import uuid
import json
import time
import unidecode

def get_client_ip(request):
    if not request:
        return None
    if not hasattr(request, 'META'):
        return None
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def get_user_agent(request):
    if request:
        if hasattr(request, 'META'):
            return request.META.get('HTTP_USER_AGENT', '')
    return ''


def get_platform(request):
    if not request:
        return Platforms.OTHER
    for platform in Platforms.choices:
        if platform[0] in get_user_agent(request).lower():
            return platform[0]
    return Platforms.OTHER


def get_browser(request):
    if not request:
        return Browsers.OTHER
    for browser in Browsers.choices:
        if browser[0] in get_user_agent(request).lower():
            return browser[0]
    return Browsers.OTHER


def get_unique_key(request, ip_address, force_update=False):
    if not request:
        return generate_random_uuid()
    if not hasattr(request, 'session'):
        return generate_random_uuid()
    if force_update:
        unique_key = None
    else:
        unique_key = request.session.get('unique_key', None)
        if unique_key:
            try:
                unique_key = uuid.UUID(unique_key)
            except Exception as e:
                unique_key = None

    if not unique_key or force_update:
        user = None
        if request:
            if request.user:
                if request.user.is_authenticated:
                    user = request.user
                    existing_logs = ActionLog.objects.filter(Q(user=request.user) | Q(ip_address=ip_address))
        if not user:
            existing_logs = ActionLog.objects.filter(ip_address=ip_address)

        if existing_logs.exists():
            unique_key = existing_logs.first().unique_key
            if request.user.is_authenticated:
                previous_logs_of_user = ActionLog.objects.filter(
                    Q(user=request.user) | Q(ip_address=ip_address),
                    ~Q(unique_key=unique_key),
                )
                if previous_logs_of_user.exists():
                    previous_logs_of_user.update(unique_key=unique_key)
            else:
                previous_logs_of_user = ActionLog.objects.filter(
                    Q(ip_address=ip_address),
                    ~Q(unique_key=unique_key),
                )
                if previous_logs_of_user.exists():
                    previous_logs_of_user.update(unique_key=unique_key)

    if not isinstance(unique_key, uuid.UUID):
        unique_key = generate_random_uuid()

    request.session['unique_key'] = str(unique_key)
    return unique_key


def create_action_log(request, action, success=True, message='', data=None, force_update=False):
    ip_address = get_client_ip(request)
    unique_key = get_unique_key(request, ip_address, force_update)
    if request:
        post_data = request.POST
        if not post_data:
            if hasattr(request, 'data'):
                post_data = request.data

        if data is None:
            data = dict(post_data) if post_data else data
        else:
            if post_data:
                data.update({
                    'POST': dict(post_data),
                })
        get_params = request.GET.dict() if request.GET else {}
        user = request.user if request.user.is_authenticated else None
        method = request.method
        path = request.path
    else:
        get_params = {}
        user = None
        method = 'UNKNOWN'
        path = ''
    action = action[:255]
    path = path[:255]
    try:
        if data:
            data = json.dumps(data, cls=DjangoJSONEncoder)
    except Exception as e:
        data = {'serialize_error': str(e), **data}
    try:
        ActionLog.objects.create(
            user=user,
            action=action,
            message=message,
            method=method,
            success=success,
            path=path,
            data=data,
            get_params=get_params,
            platform=get_platform(request),
            browser=get_browser(request),
            ip_address=ip_address,
            unique_key=unique_key,
            user_agent=get_user_agent(request)[0:255],
        )
    except:
        ActionLog.objects.create(
            user=user,
            action=f'ERROR: {action}',
            message=str(traceback.format_exc()) + '\n\n' + str(message),
            method=method,
            success=False,
            path=path,
            data=None,
            get_params=None,
            platform=get_platform(request),
            browser=get_browser(request),
            ip_address=ip_address,
            unique_key=unique_key,
            user_agent=get_user_agent(request)[0:255],
        )


def recaptcha_check(recaptcha_response):
    if settings.DEBUG:
        return True
    try:
        verify_url = 'https://www.google.com/recaptcha/api/siteverify'
        value = {
            'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
            'response': recaptcha_response
        }
        response = requests.post(verify_url, value, headers={'Content-Type': 'application/x-www-form-urlencoded'})
        result = response.json()
        if result.get('success') is True:
            return True
        else:
            return {'status': result.get('success'), 'reason': result.get('error-codes')}
    except Exception as e:
        return {'status': False, 'reason': 'Unknown error. Error: ' + str(e)}


def random_digits(length=6):
    return ''.join(random.choices(string.digits, k=length))
    # return ''.join(random.choice(string.digits) for i in range(length))
    # return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))


def random_string(length=6, uppercase=False):
    if uppercase:
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
    else:
        return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))


def generate_random_uuid():
    return str(uuid.uuid4())


def get_html_message(plain_message, html_message):
    if plain_message and not html_message:
        html_message = plain_message.replace('\n', '<br>')
    elif html_message and not plain_message:
        plain_message = strip_tags(html_message)
    elif not plain_message and not html_message:
        plain_message = ''
        html_message = ''

    return plain_message, html_message


def check_repeated_chars(check_string, recurrent_chars=8):
    # Create a dictionary to store the count of each character
    char_count = {}

    # Loop through each character in the string and count its occurrences
    for char in check_string:
        if char in char_count:
            char_count[char] += 1
        else:
            char_count[char] = 1

        # If any character count reaches recurrent_chars, raise a flag
        if char_count[char] >= recurrent_chars:
            return True

    return False


def convert_to_latin(turkish_string):
    if not turkish_string:
        return ''
    # Convert to Latin characters
    latin_string = unidecode.unidecode(turkish_string)
    return latin_string


def sanitize_object(obj):
    def serialize_field(value):
        if isinstance(value, Model):
            return {'id': value.id, 'name': value.name}
        return value

    cleaned_data = {key: serialize_field(value) for key, value in obj.items()}

    try:
        return json.dumps(cleaned_data, cls=DjangoJSONEncoder)
    except Exception as e:
        return {'sanitize_error': str(e)}


def remove_tag(text, tag):
    text = text \
        .replace('\n', ' ') \
        .replace('\r', ' ')
    while f'<{tag}' in text:
        contents = text.split(f'<{tag}', 1)
        text = contents[0]
        if len(contents) > 1:
            end = contents[1].find('>')
            text += contents[1][end + 1:]
    return text


def remove_all_tags(text):
    text = text \
        .replace('\n', ' ') \
        .replace('\r', ' ')
    while '<' in text:
        contents = text.split('<', 1)
        text = contents[0]
        if len(contents) > 1:
            end = contents[1].find('>')
            text += contents[1][end + 1:]
    return text


def custom_validation(request, FORM_CLASS, csrf_check=True):
    if request.method != 'POST':
        return True

    post_data = request.POST
    if not post_data:
        if hasattr(request, 'data'):
            post_data = request.data

    block_user = False

    if csrf_check:
        csrfmiddlewaretoken = post_data.get('csrfmiddlewaretoken')
        if not csrfmiddlewaretoken:
            create_action_log(request, 'custom_validation', False, message='csrfmiddlewaretoken not found.')
            block_user = True

    if not block_user:
        data_names = list(post_data.keys())
        if 'csrfmiddlewaretoken' in data_names:
            data_names.remove('csrfmiddlewaretoken')

        boolean_fields = []

        form_instance = FORM_CLASS()
        field_names = list(form_instance.fields.keys())

        for field_name in field_names:
            field = form_instance.fields[field_name]
            if isinstance(field, forms.BooleanField):
                boolean_fields.append(field_name)

        for data_name in data_names:
            if data_name in boolean_fields:
                continue
            if data_name not in field_names:
                create_action_log(request, 'custom_validation', False, message=f'Unknown field: {data_name}')
                block_user = True
                break

        if not block_user:
            for field_name in field_names:
                if field_name in boolean_fields:
                    continue
                if field_name not in data_names:
                    create_action_log(request, 'custom_validation', False, message=f'Missing field: {field_name}')
                    block_user = True
                    break

    if block_user:
        BlockedUser.objects.create(
            user=request.user if request.user.is_authenticated else None,
            ip_address=get_client_ip(request),
            # phone=request.user.phone if request.user.is_authenticated else '',
            permanent=True,
        )
        return False

    return True


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
