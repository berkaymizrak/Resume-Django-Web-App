from core.models import BaseAbstractModel
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

    class Meta:
        verbose_name_plural = 'Redirect Slugs'
        verbose_name = 'Redirect Slug'
        ordering = ('-created_at',)

    def __str__(self):
        return 'Redirect Slug: %s' % self.slug
