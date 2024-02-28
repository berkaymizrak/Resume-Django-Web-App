from django.db import models
from django.utils.translation import gettext_lazy as _


class Platforms(models.TextChoices):
    ANDROID = ('android', 'Android')
    IOS = ('ios', 'iOS')
    WINDOWS = ('windows', 'Windows')
    LINUX = ('linux', 'Linux')
    MAC = ('mac', 'Mac')
    MOBILE = ('mobile', _('Mobile'))  # when can not parse os
    WEB = ('web', 'Web')  # when can not parse os
    OTHER = ('other', _('Other'))


class Browsers(models.TextChoices):
    CHROME = ('chrome', 'Chrome')
    FIREFOX = ('firefox', 'Firefox')
    SAFARI = ('safari', 'Safari')
    EDGE = ('edge', 'Edge')
    IE = ('ie', 'IE')
    OPERA = ('opera', 'Opera')
    OTHER = ('other', _('Other'))
