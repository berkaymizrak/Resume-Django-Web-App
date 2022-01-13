from django.shortcuts import render
from user.models import *
from user.forms import *
from django.conf import settings

from django.shortcuts import render, redirect
from django.utils.safestring import mark_safe

import requests
from django.http import JsonResponse

# from django.core.files.storage import FileSystemStorage
# from django.core.files.storage import default_storage
import os
from resume.custom_storages import MediaStorage, ImageSettingStorage, DocumentStorage

from .decorators import *
from django.contrib.auth.decorators import user_passes_test
from django.views.decorators.csrf import csrf_exempt

from django.http import Http404
from django.db.models import Q

from user import utils

# Create your views here.


def layout(request):
    show_intro = request.session.get('show_intro', None)

    site_title = utils.get_parameter('site_title')
    home_detail_title = utils.get_parameter('home_detail_title')
    site_description = utils.get_parameter('site_description')

    site_favicon = utils.get_image('site_favicon')
    site_logo = utils.get_image('site_logo')
    site_logo_height = utils.get_parameter('site_logo_height', 'int')
    site_overlay_logo = utils.get_image('site_overlay_logo')
    site_overlay_logo_width = utils.get_parameter('site_overlay_logo_width', 'int')

    context = {
        'show_intro': show_intro,
        'site_title': site_title,
        'home_detail_title': home_detail_title,
        'site_description': site_description,
        'site_favicon': site_favicon,
        'site_logo': site_logo,
        'site_overlay_logo': site_overlay_logo,
        'site_logo_height': site_logo_height,
        'site_overlay_logo_width': site_overlay_logo_width,
        'DEFAULT_PNG': settings.DEFAULT_PNG,
    }
    return context


def index(request):
    form = ContactForm(request.POST or None)
    if request.method == 'POST':
        context = {
            'success': False,
            'message': '',
        }
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
                subject = form.cleaned_data['subject']
                message = form.cleaned_data['message']

                message_context = 'Message received.\n\n' \
                                  'Name: %s\n' \
                                  'Subject: %s\n' \
                                  'Email: %s\n' \
                                  'Message: %s' % (name, subject, email, message)

                utils.send_mail_check(
                    request=request,
                    name=name,
                    subject='Message Received',
                    message=message_context,
                    to=settings.DEFAULT_FROM_EMAIL,
                    reply_to=email,
                )
                utils.send_mail_check(
                    request=request,
                    name=name,
                    subject='Message Received',
                    message=message_context,
                    to=email,
                )
                context['success'] = True
                context['message'] = 'Your message is successfully sent...'
            else:
                context['success'] = False
                context['message'] = 'Invalid reCAPTCHA. Please try again.'
        else:
            context['success'] = False
            context['message'] = 'Please fill all required fields.'
        return JsonResponse(context)

    site_title = utils.get_parameter('site_title')
    site_description = utils.get_parameter('site_description')
    person_name = utils.get_parameter('person_name')
    person_position = utils.get_parameter('person_position')
    person_description = utils.get_parameter('person_description')
    person_image = utils.get_image('person_image')
    header_logo = utils.get_image('header_logo')

    skills = Skill.objects.all()
    skills_mapped = {}
    for elem in skills:
        if elem.skill_type:
            if elem.skill_type.name not in skills_mapped.keys():
                skills_mapped[elem.skill_type.name] = [elem]
            else:
                skills_mapped[elem.skill_type.name].append(elem)

    print(skills_mapped)
    social_medias = SocialMedia.objects.all()
    documents = Document.objects.filter(show_on_page=True)

    context = {
        'skills_mapped': skills_mapped,
        'social_medias': social_medias,
        'documents': documents,

        'site_title': site_title,
        'site_description': site_description,
        'person_name': person_name,
        'person_position': person_position,
        'person_description': person_description,
        'person_image': person_image,
        'header_logo': header_logo,

        'form': form,
        'GOOGLE_RECAPTCHA_SITE_KEY': settings.GOOGLE_RECAPTCHA_SITE_KEY,
    }
    return render(request, 'index.html', context=context)


def special_links(request, slug):
    try:
        object = ImageSetting.objects.get(name=slug)
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
        'reason': reason,
    }
    return render(request, '403.html', context=context)


