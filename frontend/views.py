from datetime import datetime
from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse
from core import models as core_models
from core import forms as core_forms
from frontend import models
from core import utils
import requests


# Create your views here.


def index(request):
    form = core_forms.ContactForm(request.POST or None)
    if request.method == 'POST':
        context = {
            'success': False,
            'message': '',
        }
        ''' reCAPTCHA validation '''
        recaptcha_response = request.POST.get('g-recaptcha-response')
        data = {
            'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
            'response': recaptcha_response
        }
        r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
        result = r.json()

        if result['success']:
            context = form.send_mail()
        else:
            context['success'] = False
            context['message'] = 'Invalid reCAPTCHA. Please try again.'
        return JsonResponse(context)

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


def nikah(request):
    event_date = datetime.strptime('2023-05-20 14:00:00', '%Y-%m-%d %H:%M:%S')

    context = {
        'event_date': event_date,
    }
    return render(request, 'invitation/nikah.html', context=context)


def dugun(request):
    event_date = datetime.strptime('2023-05-21 14:30:00', '%Y-%m-%d %H:%M:%S')

    context = {
        'event_date': event_date,
    }
    return render(request, 'invitation2/dugun.html', context=context)
