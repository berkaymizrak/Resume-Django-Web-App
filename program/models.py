from core.models import AbstractModel
from django.db import models


# Create your models here.


class ExternalProgram(AbstractModel):
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
        verbose_name_plural = 'External Program Settings'
        verbose_name = 'External Program Setting'
        ordering = ('name',)

    def __str__(self):
        return f'External-Setting: {self.name}'


class ExternalLogs(AbstractModel):
    name = models.CharField(
        default='',
        max_length=255,
        verbose_name='Name',
        help_text='',
        blank=True,
    )
    parameter = models.TextField(
        default='',
        verbose_name='Parameter',
        help_text='',
        blank=True,
    )
    program = models.CharField(
        default='',
        max_length=255,
        verbose_name='Program',
        help_text='',
        blank=True,
    )
    ip_address = models.GenericIPAddressField(
        default='',
        verbose_name='IP Address',
        help_text='',
        blank=True,
        null=True,
    )
    success = models.BooleanField(
        default=False,
        verbose_name='Success',
        help_text='',
    )

    class Meta:
        verbose_name_plural = 'External Program Logs'
        verbose_name = 'External Program Log'
        ordering = ('-created_date',)

    def __str__(self):
        return f'External Log: {self.name}'
