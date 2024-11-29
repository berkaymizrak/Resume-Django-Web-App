from core.utils import create_action_log, get_parameter, get_image
from django.conf import settings
from django.shortcuts import render
from django.utils import timezone
from frontend import models as fr_models


# Create your views here.


def layout(request):
    site_title = get_parameter('site_title')
    home_detail_title = get_parameter('home_detail_title')
    meta_description = get_parameter('meta_description')
    site_keywords = get_parameter('site_keywords')
    google_analytics_tracking_id = get_parameter('google_analytics_tracking_id')

    og_image = get_image('og_image')
    header_logo = get_image('header_logo')

    coupons = fr_models.CourseCoupons.objects.filter(
        is_active=True,
        expiration_date__gte=timezone.now(),
        start_date__lte=timezone.now(),
    )

    context = {
        'STATIC_VERSION': settings.STATIC_VERSION,
        'site_name': settings.SITE_NAME,
        # 'meta_keywords': settings.META_KEYWORDS,
        # 'meta_description': settings.META_DESCRIPTION,
        'site_domain': settings.SITE_DOMAIN,
        'language_code': settings.LANGUAGE_CODE.split('-')[0],
        'DEBUG': settings.DEBUG,
        'google_recaptcha_site_key': settings.GOOGLE_RECAPTCHA_SITE_KEY,

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
    create_action_log(request, 'csrf_failure', False)
    return redirect('index')


def maintenance(request):
    if not settings.MAINTENANCE_MODE:
        return redirect('landing')
    create_action_log(request, 'maintenance')
    context = {
    }
    return render(request, '503.html', context=context)


def blocked_user(request):
    create_action_log(request, 'blocked_user', False)
    return render(request, '403.html')
