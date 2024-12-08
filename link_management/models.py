from core.models import BaseAbstractModel
from django.conf import settings
from django.db import models

# Create your models here.


class RedirectSlug(BaseAbstractModel):
    slug = models.SlugField(
        max_length=255,
        verbose_name='Slug',
        help_text='',
        unique=True,
    )
    new_url = models.URLField(
        max_length=255,
        verbose_name='New URL',
        help_text='',
    )

    class Meta(BaseAbstractModel.Meta):
        verbose_name_plural = 'Redirect Slugs'
        verbose_name = 'Redirect Slug'

    def __str__(self):
        return self.slug

    @property
    def redirect_url(self):
        return f'https://{settings.SITE_DOMAIN}/r/{self.slug}/'
