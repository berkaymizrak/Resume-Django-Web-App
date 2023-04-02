from django.conf import settings
from django.db.models import Count, CharField
from django.db.models.functions import Concat
from django.http import JsonResponse, Http404
from django.shortcuts import render
from django.utils import timezone
from user.decorators import *
from user import forms
from user import models
from user import utils
import requests


# Create your views here.


def layout(request):
    site_title = utils.get_parameter('site_title')
    home_detail_title = utils.get_parameter('home_detail_title')
    meta_description = utils.get_parameter('meta_description')
    site_keywords = utils.get_parameter('site_keywords')
    google_analytics_tracking_id = utils.get_parameter('google_analytics_tracking_id')

    og_image = utils.get_image('og_image')
    header_logo = utils.get_image('header_logo')

    coupons = models.CourseCoupons.objects.filter(is_active=True, expiration_date__gt=timezone.now())

    context = {
        'header_logo': header_logo,
        'site_title': site_title,
        'home_detail_title': home_detail_title,
        'og_image': og_image,
        'site_keywords': site_keywords,
        'meta_description': meta_description,
        'google_analytics_tracking_id': google_analytics_tracking_id,
        'DEFAULT_PNG': settings.DEFAULT_PNG,
        'GOOGLE_RECAPTCHA_SITE_KEY': settings.GOOGLE_RECAPTCHA_SITE_KEY,
        'coupons': coupons,
    }
    return context


def index(request):
    form = forms.ContactForm(request.POST or None)
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
    documents = models.Document.objects.filter(show_on_page=True)

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
    """
    Checks first if slug is in Document objects. If not then checks in images.
    Returns the file of object from slug field.
    """

    obj = None
    obj_type = None
    try:
        redirect_source = 'popup' if '_popup' in slug else 'direct_link'
        slug = slug.replace('_popup', '')
        obj = models.RedirectSlug.objects.get(slug=slug)
        try:
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                ipaddress = x_forwarded_for.split(',')[-1].strip()
            else:
                ipaddress = request.META.get('REMOTE_ADDR')
            models.Statistics.objects.create(
                statistic_type='RedirectSlug',
                action=f'Click slug: {slug}',
                source=redirect_source,
                ip_address=ipaddress,
                user_agent=request.META.get('HTTP_USER_AGENT'),
            )
        except:
            pass
        return redirect(obj.new_url)
    except models.RedirectSlug.DoesNotExist:
        pass

    try:
        obj = models.Document.objects.get(name=slug)
        obj_type = 'doc'
    except models.Document.DoesNotExist:
        pass

    if not obj:
        try:
            obj = models.ImageSetting.objects.get(name=slug)
            obj_type = 'image'
        except models.ImageSetting.DoesNotExist:
            pass

    if obj:
        if obj_type == 'doc':
            if obj.file:
                return redirect(obj.file.url)
        elif obj_type == 'image':
            if obj.file:
                context = {
                    'object': obj,
                }
                return render(request, 'image.html', context=context)
        return redirect('index')
    else:
        raise Http404


def csrf_failure(request, reason=''):
    context = {
        'reason': reason,
    }
    return render(request, '403.html', context=context)


@login_required_redirect
def statistics(request):
    statistics = models.Statistics.objects.all()
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
    return render(request, 'statistics.html', context=context)
