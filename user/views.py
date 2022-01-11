from django.shortcuts import render
from user.models import *
from user.forms import *
from django.conf import settings

from django.shortcuts import render, redirect
from django.contrib import messages

from django.core.mail import EmailMessage, send_mail
from django.utils.safestring import mark_safe

import requests
from django.http import JsonResponse

# from django.core.files.storage import FileSystemStorage
# from django.core.files.storage import default_storage
import os
from resume.custom_storages import MediaStorage, ImageSettingsStorage, DocumentStorage

from .decorators import *
from django.contrib.auth.decorators import user_passes_test
from django.views.decorators.csrf import csrf_exempt

from django.http import Http404
from django.db.models import Q

from user import utils

# Create your views here.


def send_mail_check(request, name, subject, message, to, reply_to=settings.DEFAULT_FROM_EMAIL):
    success = True
    error_message = None

    try:
        email = EmailMessage(
            subject,
            message,
            to=[to],
            reply_to=[reply_to]
        )
        email.send()
    except Exception as e:
        success = False
        error_message = str(e)

    Messages.objects.create(
        name=name,
        email=to,
        message=message,
        error_message=error_message,
        success=success,
    )


def layout(request):
    show_intro = request.session.get('show_intro', None)

    site_title = utils.get_parameter('site_title')
    site_description = utils.get_parameter('site_description')

    site_favicon = utils.get_image('site_favicon')
    site_logo = utils.get_image('site_logo')
    site_logo_height = utils.get_parameter('site_logo_height', 'int')
    site_overlay_logo = utils.get_image('site_overlay_logo')
    site_overlay_logo_width = utils.get_parameter('site_overlay_logo_width', 'int')

    context = {
        'show_intro': show_intro,
        'site_title': site_title,
        'site_description': site_description,
        'site_favicon': site_favicon,
        'site_logo': site_logo,
        'site_overlay_logo': site_overlay_logo,
        'site_logo_height': site_logo_height,
        'site_overlay_logo_width': site_overlay_logo_width,
        'DEFAULT_PNG': settings.DEFAULT_PNG,
    }
    return context


@csrf_exempt
@login_required_redirect
@user_passes_test(lambda u: u.is_superuser)
def ajax_delete_image(request):
    image_name = request.POST.get("image_name", None)
    object_id = request.POST.get("object_id", None)
    model_param = request.POST.get("model_param", None)

    model, media_storage = parse_model_details(model_param)

    if model:
        if model == Document:
            try:
                object = model.objects.get(file=image_name)
                object.delete()
                deleted = True
            except:
                deleted = delete_old_file(model, media_storage=media_storage, path=image_name)

            success = True
        else:
            success = False
            deleted = False
    else:
        success = False
        deleted = False

    context = {
        'success': success,
        'deleted': deleted,
    }
    return JsonResponse(context)


def check_create_file_name(model, media_storage, file_name):
    add_val = 2
    added = False
    while True:
        file_name = media_storage.get_available_name(file_name)

        try:
            object = model.objects.get(file=file_name)
            if '.' in file_name:
                file_base_name = file_name.rsplit('.', 1)[0]
                file_extension = file_name.rsplit('.', 1)[-1]
                file_extension = '.' + file_extension
            else:
                file_base_name = file_name
                file_extension = ''

            if added:
                add_val += 1
                file_base_name = file_base_name[:-2]
            else:
                added = True
            file_name = file_base_name + '_' + str(add_val) + file_extension
        except:
            break

    return file_name


@csrf_exempt
@login_required_redirect
@user_passes_test(lambda u: u.is_superuser)
def ajax_create_image_name(request):
    image_name = request.POST.get("image_name", None)
    model_param = request.POST.get("model_param", None)

    model, media_storage = parse_model_details(model_param)

    if model:
        image_name = check_create_file_name(model, media_storage, image_name)

        success = True
    else:
        success = False
        image_name = None

    context = {
        'success': success,
        'image_name': image_name,
    }
    return JsonResponse(context)


def parse_model_details(model_param):
    if model_param == 'image_settings':
        model = ImageSettings
        media_storage = ImageSettingsStorage()
    elif model_param == 'document':
        model = Document
        media_storage = DocumentStorage()
    else:
        model = None
        media_storage = MediaStorage()

    return model, media_storage


@csrf_exempt
@login_required_redirect
@user_passes_test(lambda u: u.is_superuser)
def ajax_upload_image(request):
    file_lists = parse_file_list(request, in_POST=False)
    # param, myfile = parse_file_list(request, in_POST=False)

    url = None
    # file_path_within_bucket = None
    save_file_name = ''

    success = False
    for param, myfile in file_lists.items():
        model, media_storage = parse_model_details(param)

        if model:
            save_file_name = check_create_file_name(model, media_storage, myfile.name)

            media_storage.save(save_file_name, myfile)
            url = media_storage.url(save_file_name)

            if model == Document:
                model.objects.create(
                    button_text='Download',
                    file=save_file_name,
                )

            success = True
        else:
            success = False

    context = {
        'success': success,
        'url': url,
        'file_name': save_file_name,
    }
    return JsonResponse(context)


def parse_file_list(request, in_POST=True):
    file_lists = {}

    if in_POST:
        loop_list = request.POST.keys()
    else:
        loop_list = request.FILES.keys()

    for elem in loop_list:
        if 'file_list_' in elem:
            param = elem.replace('file_list_', '')
            if param:
                file_lists[param] = []

    for param in list(file_lists.keys()):
        if in_POST:
            file_list = request.POST.getlist('file_list_' + param)
        else:
            file_list = request.FILES['file_list_' + param]
        file_lists[param] = file_list

    return file_lists


def index(request):
    form = ContactForm(request.POST or None)
    if request.method == 'POST':
        redirect_contact = True
        if form.is_valid():
            ''' reCAPTCHA validation '''
            recaptcha_response = request.POST.get('g-recaptcha-response')
            data = {
                'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
                'response': recaptcha_response
            }
            r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
            result = r.json()

            if result['success']:
                name = form.cleaned_data['name']
                email = form.cleaned_data['email']
                message = form.cleaned_data['message']

                message_context = 'Message received.\n\n' \
                                  'Name: %s\n' \
                                  'Email: %s\n' \
                                  'Message: %s' % (name, email, message)

                send_mail_check(request, name, 'Message Received', message_context, settings.DEFAULT_FROM_EMAIL, email, )
                send_mail_check(request, name, 'Message Received', message_context, email, )

                message = "Message successfully sent."
                messages.success(request, message)
                request.session['redirect_contact'] = True
                return redirect('index')
            else:
                message = 'Invalid reCAPTCHA. Please try again.'
                messages.error(request, message)
        else:
            mesaj = "Please fill all required fields."
            messages.error(request, mesaj)
    else:
        redirect_contact = request.session.get('redirect_contact', None)
        try:
            del request.session['redirect_contact']
        except:
            pass

    about_header = utils.get_parameter('about_header')
    about_description = utils.get_parameter('about_description')
    contact_header = utils.get_parameter('contact_header')
    contact_description = utils.get_parameter('contact_description')

    skills_1, skills_2 = utils.get_skills_table()

    features = Features.objects.all().order_by('order')

    context = {
        'skills_1': skills_1,
        'skills_2': skills_2,
        'features': features,

        'about_header': about_header,
        'about_description': about_description,
        'contact_header': contact_header,
        'contact_description': contact_description,

        'form': form,
        'redirect_contact': redirect_contact,
        'GOOGLE_RECAPTCHA_SITE_KEY': settings.GOOGLE_RECAPTCHA_SITE_KEY,
    }
    return render(request, 'index.html', context=context)


def special_links(request, slug):
    try:
        object = ImageSettings.objects.get(setting=slug)
    except:
        object = None

    if object:
        if object.file:
            context = {
                'object': object,
            }
            return render(request, 'image.html', context=context)
        else:
            return redirect('index')
    else:
        raise Http404


def csrf_failure(request, reason=""):
    context = {
        'message': 'You may be already signed in. Please refresh the page.'
    }
    return render(request, '403.html', context=context)


