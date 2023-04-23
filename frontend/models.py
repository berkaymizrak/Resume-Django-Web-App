from core.models import AbstractModel
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone


# Create your models here.


class SkillTypes(AbstractModel):
    name = models.CharField(
        default='',
        max_length=254,
        verbose_name='Name',
        help_text='',
        blank=True,
        null=True,
        unique=True,
    )

    class Meta:
        verbose_name_plural = 'Skill Types'
        verbose_name = 'Skill Type'
        ordering = ('name',)

    def __str__(self):
        return 'Skill Type: %s' % self.name


class Skill(AbstractModel):
    order = models.IntegerField(
        default=1,
        verbose_name='Order',
        blank=True,
    )
    name = models.CharField(
        default='',
        max_length=254,
        verbose_name='Name',
        help_text='',
        blank=True,
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

    class Meta:
        verbose_name_plural = 'Skills'
        verbose_name = 'Skill'
        ordering = ('order',)

    def __str__(self):
        return 'Skill: %s' % self.name


class SocialMedia(AbstractModel):
    order = models.IntegerField(
        default=1,
        verbose_name='Order',
        blank=True,
    )
    url = models.URLField(
        default='',
        max_length=254,
        verbose_name='URL',
        help_text='',
        blank=True,
    )
    icon = models.CharField(
        default='',
        max_length=254,
        verbose_name='Icon (Font Awesome)',
        help_text='https://fontawesome.com/v5.15/icons?d=gallery&p=2&m=free',
        blank=True,
    )

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


class CourseCoupons(AbstractModel):
    order = models.IntegerField(
        default=10,
        verbose_name='Order',
    )
    course_name = models.CharField(
        default='',
        max_length=255,
        verbose_name='Course Name',
        help_text='',
        blank=True,
    )
    course_url = models.URLField(
        default='',
        max_length=255,
        verbose_name='Course URL',
        help_text='',
        blank=True,
    )
    coupon_code = models.CharField(
        default='',
        max_length=255,
        verbose_name='Coupon Code',
        help_text='',
        blank=True,
    )
    original_price = models.FloatField(
        default=0,
        verbose_name='Original Price',
        help_text='',
    )
    discount_price = models.FloatField(
        default=0,
        verbose_name='Discount Price',
        help_text='',
    )
    expiration_date = models.DateTimeField(
        default=timezone.now,
        verbose_name='Expiration Date',
        help_text='',
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Is Active',
    )

    class Meta:
        verbose_name_plural = 'Course Coupons'
        verbose_name = 'Course Coupon'
        ordering = ('order',)

    def __str__(self):
        return 'Course Coupon: %s' % self.course_name
