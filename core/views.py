from django.conf import settings
from django.shortcuts import render
from django.utils import timezone
from core import utils
from frontend import models as fr_models


# Create your views here.


def layout(request):
    site_title = utils.get_parameter('site_title')
    home_detail_title = utils.get_parameter('home_detail_title')
    meta_description = utils.get_parameter('meta_description')
    site_keywords = utils.get_parameter('site_keywords')
    google_analytics_tracking_id = utils.get_parameter('google_analytics_tracking_id')

    og_image = utils.get_image('og_image')
    header_logo = utils.get_image('header_logo')

    coupons = fr_models.CourseCoupons.objects.filter(is_active=True, expiration_date__gt=timezone.now())

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


def csrf_failure(request, reason=''):
    context = {
        'reason': reason,
    }
    utils.create_action_log(request, 'csrf_failure', f'GET: {reason}', False)
    return render(request, '403.html', context=context)
