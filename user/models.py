from django.db import models, IntegrityError
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.dispatch import receiver
from django.utils.crypto import get_random_string
from django.utils.text import slugify
from resume.custom_storages import ImageSettingStorage, DocumentStorage


# Create your models here.


class GeneralSetting(models.Model):
    name = models.CharField(default='', max_length=254, verbose_name='Name', help_text='', blank=True, null=True)
    description = models.CharField(
        default='',
        max_length=254,
        verbose_name='Description',
        help_text='',
        blank=True,
        null=True,
    )
    parameter = models.TextField(default='', verbose_name='Parameter', help_text='', blank=True, null=True)

    date = models.DateTimeField(verbose_name='Created Date', blank=True, auto_now_add=True)

    class Meta:
        verbose_name_plural = 'General Settings'
        verbose_name = 'General Setting'
        ordering = ('name',)

    def __str__(self):
        return 'General Setting: %s' % self.name


class ImageSetting(models.Model):
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
        null=True,
    )
    file = models.ImageField(
        default='',
        storage=ImageSettingStorage(),
        verbose_name='Image',
        help_text='',
        blank=True,
        null=True,
    )

    date = models.DateTimeField(verbose_name='Created Date', blank=True, auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Image Settings'
        verbose_name = 'Image Setting'
        ordering = ('name',)

    def __str__(self):
        return 'Image Setting: %s' % self.name

    def save(self, *args, **kwargs):
        self.name = slugify(self.name)
        while True:
            print(self.name)
            try:
                super(ImageSetting, self).save(*args, **kwargs)
            except IntegrityError:
                self.name += get_random_string(allowed_chars="0123456789", length=2)


class Document(models.Model):
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
        null=True,
    )
    file = models.FileField(
        default='',
        storage=DocumentStorage(),
        verbose_name='Document',
        help_text='',
    )
    show_on_page = models.BooleanField(default=True, verbose_name='Show on menu')
    date = models.DateTimeField(verbose_name='Created Date', blank=True, auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Documents'
        verbose_name = 'Document'
        ordering = ('date',)

    def __str__(self):
        return 'Document: %s' % self.button_text

    def save(self, *args, **kwargs):
        self.name = slugify(self.name)
        while True:
            try:
                return super(Document, self).save(*args, **kwargs)
            except IntegrityError:
                self.name += get_random_string(allowed_chars="0123456789", length=2)


class SkillTypes(models.Model):
    name = models.CharField(
        default='',
        max_length=254,
        verbose_name='Name',
        help_text='',
        blank=True,
        null=True,
        unique=True,
    )
    date = models.DateTimeField(verbose_name='Created Date', blank=True, auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Skill Types'
        verbose_name = 'Skill Type'
        ordering = ('name',)

    def __str__(self):
        return 'Skill Type: %s' % self.name


class Skill(models.Model):
    order = models.IntegerField(default=1, verbose_name='Order', blank=True)
    name = models.CharField(
        default='',
        max_length=254,
        verbose_name='Name',
        help_text='',
        blank=True,
        null=True,
    )
    percent = models.IntegerField(
        default=50,
        verbose_name='Percent',
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )
    skill_type = models.ForeignKey(
        SkillTypes,
        default=None,
        on_delete=models.CASCADE,
        verbose_name="Skill Type",
        blank=True,
        null=True,
    )

    date = models.DateTimeField(verbose_name='Created Date', blank=True, auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Skills'
        verbose_name = 'Skill'
        ordering = ('order',)

    def __str__(self):
        return 'Skill: %s' % self.name


class SocialMedia(models.Model):
    order = models.IntegerField(default=1, verbose_name='Order', blank=True)
    url = models.URLField(default='', max_length=254, verbose_name='URL', help_text='', blank=True, null=True)
    icon = models.CharField(
        default='',
        max_length=254,
        verbose_name='Icon (Font Awesome)',
        help_text='https://fontawesome.com/v5.15/icons?d=gallery&p=2&m=free',
        blank=True,
        null=True,
    )

    date = models.DateTimeField(verbose_name='Created Date', blank=True, auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Social Medias'
        verbose_name = 'Social Media'
        ordering = ('order',)

    def __str__(self):
        return 'Social Media: %s' % self.icon

    def save(self, *args, **kwargs):
        if self.icon:
            if 'ot-circle' not in self.icon and 'class=' in self.icon:
                icon_list = self.icon.split('class=')
                if len(icon_list) >= 2:
                    icon_list[1] = icon_list[1][:1] + 'ot-circle ' + icon_list[1][1:]
                    self.icon = 'class='.join(icon_list)
        super().save(*args, **kwargs)


class Message(models.Model):
    name = models.CharField(default='', max_length=254, verbose_name='Enter Your Name', help_text='', blank=True)
    email = models.CharField(default='', max_length=254, verbose_name='Enter Email Address', help_text='', blank=True)
    subject = models.CharField(default='', max_length=254, verbose_name='Enter Subject', help_text='', blank=True)
    message = models.CharField(default='', max_length=999, verbose_name='Enter Message', help_text='', blank=True)
    error_message = models.TextField(default='', verbose_name='Error Message', help_text='', blank=True, null=True)
    success = models.BooleanField(default=True, verbose_name='Success')

    date = models.DateTimeField(blank=True, auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Messages'
        verbose_name = 'Message'
        ordering = ('-date',)

    def __str__(self):
        return 'Message: %s' % self.name


def delete_old_file(model, media_storage=None, instance=None, delete_older=False, path=None):
    # path OTHERWISE instance
    # media_storage OTHERWISE instance
    # if settings.DEBUG:
    #     return False

    if path:
        old_file_path = path
    else:
        if not instance:
            return False
        if delete_older:
            if not instance.pk:
                return False

            try:
                old_file = model.objects.get(pk=instance.pk).file
            except model.DoesNotExist:
                return False

            new_file = instance.file
            if old_file != new_file:
                pass  # WILL DELETE
            else:
                old_file = None
        else:
            old_file = instance.file

        if old_file:
            old_file_path = old_file.name
        else:
            old_file_path = None

    if old_file_path:
        if not media_storage and instance:
            media_storage = instance.file.storage
        else:
            if not media_storage:
                return False
        if media_storage.exists(old_file_path):
            media_storage.delete(old_file_path)
            return True

    return False


@receiver(models.signals.post_delete, sender=ImageSetting)
def auto_delete_file_on_delete_ImageSetting(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    delete_old_file(sender, instance=instance, delete_older=False)


@receiver(models.signals.pre_save, sender=ImageSetting)
def auto_delete_file_on_change_ImageSetting(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding `MediaFile` object is updated
    with new file.
    """
    delete_old_file(sender, instance=instance, delete_older=True)


@receiver(models.signals.post_delete, sender=Document)
def auto_delete_file_on_delete_Document(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    delete_old_file(sender, instance=instance, delete_older=False)


@receiver(models.signals.pre_save, sender=Document)
def auto_delete_file_on_change_Document(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding `MediaFile` object is updated
    with new file.
    """
    delete_old_file(sender, instance=instance, delete_older=True)
