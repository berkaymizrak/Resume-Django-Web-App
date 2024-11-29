from core import models
from core.decorators import *
from datetime import datetime
from django.conf import settings
from django.db.models import Count
from django.db.models.functions import Concat
from django.shortcuts import render, redirect
from django.http import JsonResponse
from core import models as core_models
from core import forms as core_forms
from core import utils
from core.utils import create_action_log, custom_validation, recaptcha_check
from frontend import models
import requests


# Create your views here.


def index(request):
    if not custom_validation(request, core_forms.ContactForm):
        return redirect('blocked_user')

    form = core_forms.ContactForm(request.POST or None)
    if request.method == 'POST':
        context = {
            'success': False,
            'message': '',
        }
        captcha = request.POST.get('captcha')
        if recaptcha_check(captcha) is not True:
            context['success'] = False
            context['message'] = 'Invalid reCAPTCHA. Please try again.'
        else:
            context = form.send_mail()
        create_action_log(request, 'contact_form', True,
                          data={
                              'success': context['success'],
                              'message': context['message'],
                              'POST': request.POST,
                          })
        return JsonResponse(context)
    create_action_log(request, 'landing', True)

    person_name = utils.get_parameter('person_name')
    person_position = utils.get_parameter('person_position')
    person_description = utils.get_parameter('person_description')
    person_image = utils.get_image('person_image')

    skills = models.Skill.objects.all()
    skills_mapped = {}
    for elem in skills:
        if elem.skill_type:
            if elem.skill_type.name not in skills_mapped.keys():
                skills_mapped[elem.skill_type.name] = [elem]
            else:
                skills_mapped[elem.skill_type.name].append(elem)

    social_medias = models.SocialMedia.objects.all()
    documents = core_models.Document.objects.filter(show_on_page=True)

    context = {
        'skills_mapped': skills_mapped,
        'social_medias': social_medias,
        'documents': documents,

        'person_name': person_name,
        'person_position': person_position,
        'person_description': person_description,
        'person_image': person_image,

        'form': form,
    }
    return render(request, 'index.html', context=context)


def invitation(request):
    event_date = datetime.strptime('2023-05-21 14:30:00', '%Y-%m-%d %H:%M:%S')

    create_action_log(request, 'invitation', True)
    context = {
        'event_date': event_date,
    }
    return render(request, 'invitation/invitation.html', context=context)


@login_required_redirect
def statistics(request):
    statistics = core_models.Statistics.objects.all()
    statistics_type_count = statistics.values('statistic_type').annotate(Count('statistic_type'))
    statistics_action_count = statistics.values('action').annotate(Count('action'))
    statistics_source_count = statistics.values('source').annotate(Count('source'))
    statistics_action_source_count = statistics.annotate(action_source=Concat('action', 'source')) \
        .values('statistic_type', 'action', 'source', 'action_source', ) \
        .annotate(Count('action_source'))

    context = {
        'statistics_type_count': statistics_type_count,
        'statistics_action_count': statistics_action_count,
        'statistics_source_count': statistics_source_count,
        'statistics_action_source_count': statistics_action_source_count,
    }
    create_action_log(request, 'statistics', True)
    return render(request, 'statistics.html', context=context)
