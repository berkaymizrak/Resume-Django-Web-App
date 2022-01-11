from django import template
from user.utils import get_parameter
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
def get_object_value(value):
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

