from django.shortcuts import render
from user.models import *
from user.forms import *
from django.shortcuts import render
import requests
from django.http import JsonResponse, Http404
from .decorators import *
from user import utils

# Create your views here.


def layout(request):
    site_title = utils.get_parameter('site_title')
    home_detail_title = utils.get_parameter('home_detail_title')
    meta_description = utils.get_parameter('meta_description')
    site_keywords = utils.get_parameter('site_keywords')
    google_analytics_tracking_id = utils.get_parameter('google_analytics_tracking_id')

    site_favicon = utils.get_image('site_favicon')
    og_image = utils.get_image('og_image')
    header_logo = utils.get_image('header_logo')

    context = {
        'header_logo': header_logo,
        'site_title': site_title,
        'home_detail_title': home_detail_title,
        'og_image': og_image,
        'site_keywords': site_keywords,
        'meta_description': meta_description,
        'site_favicon': site_favicon,
        'google_analytics_tracking_id': google_analytics_tracking_id,
        'DEFAULT_PNG': settings.DEFAULT_PNG,
        'GOOGLE_RECAPTCHA_SITE_KEY': settings.GOOGLE_RECAPTCHA_SITE_KEY,
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

                utils.send_mail_both(
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

    person_name = utils.get_parameter('person_name')
    person_position = utils.get_parameter('person_position')
    person_description = utils.get_parameter('person_description')
    person_image = utils.get_image('person_image')

    skills = Skill.objects.all()
    skills_mapped = {}
    for elem in skills:
        if elem.skill_type:
            if elem.skill_type.name not in skills_mapped.keys():
                skills_mapped[elem.skill_type.name] = [elem]
            else:
                skills_mapped[elem.skill_type.name].append(elem)

    social_medias = SocialMedia.objects.all()
    documents = Document.objects.filter(show_on_page=True)

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


