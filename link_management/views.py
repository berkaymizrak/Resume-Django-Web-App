from core import models as core_models
from core.decorators import *
from core.utils import create_action_log
from django.shortcuts import render
from django.http import Http404
from link_management import models


# Create your views here.


def create_statistic(request, statistic_type, action, source):
    try:
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ipaddress = x_forwarded_for.split(',')[-1].strip()
        else:
            ipaddress = request.META.get('REMOTE_ADDR')

        core_models.Statistics.objects.create(
            statistic_type=statistic_type,
            action=action,
            source=source,
            ip_address=ipaddress,
            user_agent=request.META.get('HTTP_USER_AGENT'),
        )
    except:
        pass


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
        create_statistic(request, 'RedirectSlug', f'Click slug: {slug}', redirect_source)
        return redirect(obj.new_url)
    except models.RedirectSlug.DoesNotExist:
        pass

    try:
        obj = core_models.Document.objects.get(name=slug)
        obj_type = 'doc'
    except core_models.Document.DoesNotExist:
        pass

    if not obj:
        try:
            obj = core_models.ImageSetting.objects.get(name=slug)
            obj_type = 'image'
        except core_models.ImageSetting.DoesNotExist:
            pass

    if obj:
        if obj_type == 'doc':
            if obj.file:
                create_statistic(request, 'Document', f'Click slug: {slug}', 'direct_link')
                create_action_log(request, 'special_links', f'GET doc: {slug}', True)
                return redirect(obj.file.url)
        elif obj_type == 'image':
            if obj.file:
                context = {
                    'object': obj,
                }
                create_statistic(request, 'ImageSetting', f'Click slug: {slug}', 'direct_link')
                create_action_log(request, 'special_links', f'GET image: {slug}', True)
                return render(request, 'image.html', context=context)
        create_action_log(request, 'special_links', 'GET not image or doc. Redirecting to index', False)
        return redirect('index')
    else:
        create_action_log(request, 'special_links', 'GET not found', False)
        raise Http404
