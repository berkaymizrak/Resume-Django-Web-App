from core.utils import get_parameter
from django import template
from django.conf import settings

register = template.Library()


@register.filter
def get_image_url(image):
    if image:
        try:
            if image.url:
                return image.url
            else:
                raise Exception
        except:
            return settings.DEFAULT_PNG
    else:
        return settings.DEFAULT_PNG


@register.filter
def get_document_url(file):
    if file:
        try:
            if file.url:
                return file.url
            else:
                raise Exception
        except:
            return ''
    else:
        return ''


@register.filter
def get_object_value_or_none(value):
    if value:
        return value
    else:
        return ''


@register.filter
def get_object_value_or_default(value):
    if value:
        return value
    else:
        site_title = get_parameter('site_title')
        return site_title
