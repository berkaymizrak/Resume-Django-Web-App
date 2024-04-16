from core.enums import Platforms, Browsers
from core.utils import delete_media_file
from django.db import models, IntegrityError
from django.dispatch import receiver
from django.utils.crypto import get_random_string
from django.utils.text import slugify
from django.template.defaultfilters import truncatechars
from resume.custom_storages import ImageSettingStorage, DocumentStorage
from django.contrib.auth.models import User


# Create your models here.


class AbstractModel(models.Model):
    is_deleted = models.BooleanField(default=False)
    updated_at = models.DateTimeField(
        verbose_name='Updated Date',
        blank=True,
        auto_now=True,
    )
    created_at = models.DateTimeField(
        verbose_name='Created Date',
        blank=True,
        auto_now_add=True,
    )

    class Meta:
        abstract = True


class GeneralSetting(AbstractModel):
    name = models.CharField(
        default='',
        max_length=255,
        verbose_name='Name',
        help_text='',
        blank=True,
    )
    description = models.CharField(
        default='',
        max_length=255,
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
        max_length=255,
        verbose_name='Name',
        help_text='This works as slug end of the url after domain. (https://berkaymizrak.com/xxxx)',
        blank=True,
        null=True,
        unique=True,
    )
    description = models.CharField(
        default='',
        max_length=255,
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
        max_length=255,
        verbose_name='Name',
        help_text='This works as slug end of the url after domain. (https://berkaymizrak.com/xxxx)',
        blank=True,
        null=True,
        unique=True,
    )
    button_text = models.CharField(
        default='Download',
        max_length=255,
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
        ordering = ('-created_at',)

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
        max_length=255,
        verbose_name='Enter Your Name',
        help_text='',
        blank=True,
    )
    email = models.CharField(
        default='',
        max_length=255,
        verbose_name='Enter Email Address',
        help_text='',
        blank=True,
    )
    subject = models.CharField(
        default='',
        max_length=255,
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
        ordering = ('-created_at',)

    def __str__(self):
        return 'Message: %s' % self.name


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
        ordering = ('-created_at',)

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


class ActionLog(AbstractModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None, blank=True, null=True, )
    action = models.CharField(max_length=255)
    message = models.TextField(default='', max_length=255, blank=True)
    method = models.CharField(default='', max_length=255, blank=True)
    success = models.BooleanField(default=True)
    data = models.JSONField(default=dict, blank=True, null=True)
    get_params = models.JSONField(default=dict, blank=True, null=True)
    platform = models.CharField(max_length=30, choices=Platforms.choices, default=Platforms.OTHER, )
    browser = models.CharField(max_length=30, choices=Browsers.choices, default=Browsers.OTHER, )
    user_agent = models.TextField(default='', max_length=255, blank=True)
    ip_address = models.GenericIPAddressField(default=None, blank=True, null=True, )

    def __str__(self):
        return f'{self.user} - {self.action}'

    @property
    def short_data(self):
        return truncatechars(self.data, 100)

    @property
    def short_user_agent(self):
        return truncatechars(self.user_agent, 100)

    @property
    def short_get_params(self):
        return truncatechars(self.get_params, 100)


class BlockedUser(AbstractModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None, blank=True, null=True, )
    ip_address = models.GenericIPAddressField(default=None, blank=True, null=True, )

    def __str__(self):
        return f'{self.user} - {self.ip_address}'
