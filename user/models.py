from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

from django.utils.text import slugify

from django.dispatch import receiver
# import os
# from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.core.files.storage import default_storage
from resume.custom_storages import MediaStorage, ImageSettingsStorage, DocumentStorage


# Create your models here.


class GeneralSettings(models.Model):
    setting = models.CharField(default='', max_length=254, verbose_name='Ayar', help_text='', blank=True, null=True)
    description = models.CharField(default='', max_length=254, verbose_name='Açıklama', help_text='', blank=True,
                                   null=True)
    parameter = models.TextField(default='', verbose_name='Parametre', help_text='', blank=True, null=True)

    date = models.DateTimeField(verbose_name='Oluşturma Tarihi', blank=True, auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Genel Ayarlar'
        verbose_name = 'Genel Ayar'
        ordering = ('setting',)

    def __str__(self):
        return 'Genel Ayar: %s' % self.setting


class ImageSettings(models.Model):
    setting = models.CharField(default='', max_length=254, verbose_name='Ayar', help_text='', blank=True, null=True)
    description = models.CharField(default='', max_length=254, verbose_name='Açıklama', help_text='', blank=True,
                                   null=True)
    file = models.ImageField(default='',
                             storage=ImageSettingsStorage(),
                             verbose_name='Görsel', help_text='', blank=True, null=True)

    date = models.DateTimeField(verbose_name='Oluşturma Tarihi', blank=True, auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Görsel Ayarlar'
        verbose_name = 'Görsel Ayar'
        ordering = ('setting',)

    def __str__(self):
        return 'Görsel Ayar: %s' % self.setting


class Document(models.Model):
    button_text = models.CharField(default='Download', max_length=254, verbose_name='Buton Yazısı', help_text='',
                                   blank=True, null=True)
    file = models.FileField(default='',
                            storage=DocumentStorage(),
                            verbose_name='Döküman', help_text='')

    date = models.DateTimeField(verbose_name='Oluşturma Tarihi', blank=True, auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Döküman'
        verbose_name = 'Döküman'
        ordering = ('date',)

    def __str__(self):
        return 'Döküman: %s' % self.button_text


class Skills(models.Model):
    order = models.IntegerField(default=1, verbose_name='Sıralama', blank=True)
    header = models.CharField(default='', max_length=254, verbose_name='Yetenek Adı', help_text='', blank=True,
                              null=True)
    percent = models.IntegerField(default=50, verbose_name='Yüzdelik (%)',
                                  validators=[MinValueValidator(0), MaxValueValidator(100)])

    date = models.DateTimeField(verbose_name='Oluşturma Tarihi', blank=True, auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Yetenek'
        verbose_name = 'Yetenek'
        ordering = ('order',)

    def __str__(self):
        return 'Yetenek: %s' % self.header


class Features(models.Model):
    order = models.IntegerField(default=1, verbose_name='Sıralama', blank=True)
    header = models.CharField(default='', max_length=254, verbose_name='Özellik', help_text='', blank=True, null=True)
    icon = models.CharField(default='', max_length=254, verbose_name='İkon (Font Awesome)',
                            help_text='https://fontawesome.com/v5.15/icons?d=gallery&p=2&m=free', blank=True, null=True)

    date = models.DateTimeField(verbose_name='Oluşturma Tarihi', blank=True, auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Özellikler'
        verbose_name = 'Özellik'
        ordering = ('order',)

    def __str__(self):
        return 'Özellik: %s' % self.header

    def save(self, *args, **kwargs):
        if 'ot-circle' not in self.icon and 'class=' in self.icon:
            icon_list = self.icon.split('class=')
            if len(icon_list) >= 2:
                icon_list[1] = icon_list[1][:1] + 'ot-circle ' + icon_list[1][1:]
                self.icon = 'class='.join(icon_list)
        super().save(*args, **kwargs)


class Messages(models.Model):
    name = models.CharField(default='', max_length=254, verbose_name='Ad Soyad', help_text='', blank=True)
    email = models.CharField(default='', max_length=254, verbose_name='E-posta', help_text='', blank=True)
    # subject = models.CharField(default='', max_length=254, verbose_name='Konu', help_text='', blank=True)
    message = models.CharField(default='', max_length=999, verbose_name='Mesajınız', help_text='', blank=True)
    error_message = models.TextField(default='', verbose_name='Hata Mesajı', help_text='', blank=True, null=True)
    success = models.BooleanField(default=True, verbose_name='Başarılı')

    date = models.DateTimeField(blank=True, auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Mesajlar'
        verbose_name = 'Mesaj'
        ordering = ('-date',)

    def __str__(self):
        return 'Mesaj: %s' % self.name


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


@receiver(models.signals.post_delete, sender=ImageSettings)
def auto_delete_file_on_delete_ImageSettings(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    delete_old_file(sender, instance=instance, delete_older=False)


@receiver(models.signals.pre_save, sender=ImageSettings)
def auto_delete_file_on_change_ImageSettings(sender, instance, **kwargs):
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
