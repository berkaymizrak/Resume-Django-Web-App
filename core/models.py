from core.utils import delete_media_file
from django.db import models, IntegrityError
from django.dispatch import receiver
from django.utils.crypto import get_random_string
from django.utils.text import slugify
from resume.custom_storages import ImageSettingStorage, DocumentStorage


# Create your models here.


class AbstractModel(models.Model):
    updated_date = models.DateTimeField(
        verbose_name='Updated Date',
        blank=True,
        auto_now=True,
    )
    created_date = models.DateTimeField(
        verbose_name='Created Date',
        blank=True,
        auto_now_add=True,
    )

    class Meta:
        abstract = True


class GeneralSetting(AbstractModel):
    name = models.CharField(
        default='',
        max_length=254,
        verbose_name='Name',
        help_text='',
        blank=True,
    )
    description = models.CharField(
        default='',
        max_length=254,
        verbose_name='Description',
        help_text='',
        blank=True,
    )
    parameter = models.TextField(
        default='',
        verbose_name='Parameter',
        help_text='',
        blank=True,
    )

    class Meta:
        verbose_name_plural = 'General Settings'
        verbose_name = 'General Setting'
        ordering = ('name',)

    def __str__(self):
        return 'General Setting: %s' % self.name


class ImageSetting(AbstractModel):
    name = models.CharField(
        default='',
        max_length=254,
        verbose_name='Name',
        help_text='This works as slug end of the url after domain. (https://berkaymizrak.com/xxxx)',
        blank=True,
        null=True,
        unique=True,
    )
    description = models.CharField(
        default='',
        max_length=254,
        verbose_name='Description',
        help_text='',
        blank=True,
    )
    file = models.ImageField(
        default='',
        storage=ImageSettingStorage(),
        verbose_name='Image',
        help_text='',
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name_plural = 'Image Settings'
        verbose_name = 'Image Setting'
        ordering = ('name',)

    def __str__(self):
        return 'Image Setting: %s' % self.name

    def save(self, *args, **kwargs):
        self.name = slugify(self.name)
        while True:
            try:
                return super(ImageSetting, self).save(*args, **kwargs)
            except IntegrityError:
                self.name += get_random_string(allowed_chars='0123456789', length=2)


class Document(AbstractModel):
    name = models.CharField(
        default='',
        max_length=254,
        verbose_name='Name',
        help_text='This works as slug end of the url after domain. (https://berkaymizrak.com/xxxx)',
        blank=True,
        null=True,
        unique=True,
    )
    button_text = models.CharField(
        default='Download',
        max_length=254,
        verbose_name='Button Text',
        help_text='',
        blank=True,
    )
    file = models.FileField(
        default='',
        storage=DocumentStorage(),
        verbose_name='Document',
        help_text='',
    )
    show_on_page = models.BooleanField(
        default=True,
        verbose_name='Show on menu',
    )

    class Meta:
        verbose_name_plural = 'Documents'
        verbose_name = 'Document'
        ordering = ('-created_date',)

    def __str__(self):
        return 'Document: %s' % self.button_text

    def save(self, *args, **kwargs):
        self.name = slugify(self.name)
        while True:
            try:
                return super(Document, self).save(*args, **kwargs)
            except IntegrityError:
                self.name += get_random_string(allowed_chars='0123456789', length=2)


class Message(AbstractModel):
    name = models.CharField(
        default='',
        max_length=254,
        verbose_name='Enter Your Name',
        help_text='',
        blank=True,
    )
    email = models.CharField(
        default='',
        max_length=254,
        verbose_name='Enter Email Address',
        help_text='',
        blank=True,
    )
    subject = models.CharField(
        default='',
        max_length=254,
        verbose_name='Enter Subject',
        help_text='',
        blank=True,
    )
    message = models.CharField(
        default='',
        max_length=999,
        verbose_name='Enter Message',
        help_text='',
        blank=True,
    )
    error_message = models.TextField(
        default='',
        verbose_name='Error Message',
        help_text='',
        blank=True,
        null=True,
    )
    success = models.BooleanField(
        default=True,
        verbose_name='Success',
    )

    class Meta:
        verbose_name_plural = 'Messages'
        verbose_name = 'Message'
        ordering = ('-created_date',)

    def __str__(self):
        return 'Message: %s' % self.name


# TODO REMOVE THIS MODEL AFTER FIRST MIGRATION
class RedirectSlug(AbstractModel):
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
        ordering = ('-created_date',)

    def __str__(self):
        return 'Redirect Slug: %s' % self.slug


class Statistics(AbstractModel):
    statistic_type = models.CharField(
        default='',
        max_length=255,
        verbose_name='Statistic Type',
        help_text='',
        blank=True,
    )
    action = models.CharField(
        default='',
        max_length=255,
        verbose_name='Action',
        help_text='',
        blank=True,
    )
    source = models.CharField(
        default='',
        max_length=255,
        verbose_name='Source',
        help_text='',
        blank=True,
    )
    ip_address = models.GenericIPAddressField(
        default=None,
        verbose_name='IP Address',
        help_text='',
        blank=True,
        null=True,
    )
    user_agent = models.CharField(
        default='',
        max_length=255,
        verbose_name='User Agent',
        help_text='',
        blank=True,
    )

    class Meta:
        verbose_name_plural = 'Statistics'
        verbose_name = 'Statistic'
        ordering = ('-created_date',)

    def __str__(self):
        return 'Statistic: %s - %s' % (self.statistic_type, self.action)


@receiver(models.signals.post_delete, sender=ImageSetting)
@receiver(models.signals.post_delete, sender=Document)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    delete_media_file(sender, instance=instance, delete_older=False)


@receiver(models.signals.pre_save, sender=ImageSetting)
@receiver(models.signals.pre_save, sender=Document)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding `MediaFile` object is updated
    with new file.
    """
    delete_media_file(sender, instance=instance, delete_older=True)
