from core.admin import AbstractAdmin, create_resource
from django.contrib import admin
from frontend import models
from frontend import forms


# Register your models here.


@admin.register(models.Skill)
class SkillAdmin(AbstractAdmin):
    resource_class = create_resource(models.Skill)
    list_display = ['id', 'order', 'name', 'percent', 'skill_type', 'updated_at', 'created_at', ]
    list_filter = AbstractAdmin.list_filter
    list_editable = ['order', 'name', 'percent', 'skill_type', ]
    search_fields = ['name', ]
    form = forms.SkillAdminForm


@admin.register(models.SkillTypes)
class SkillTypesAdmin(AbstractAdmin):
    resource_class = create_resource(models.SkillTypes)
    list_display = ['id', 'name', 'updated_at', 'created_at', ]
    list_filter = AbstractAdmin.list_filter
    list_editable = ['name', ]
    search_fields = ['name', ]


@admin.register(models.SocialMedia)
class SocialMediaAdmin(AbstractAdmin):
    resource_class = create_resource(models.SocialMedia)
    list_display = ['id', 'order', 'url', 'icon', 'updated_at', 'created_at', ]
    list_filter = AbstractAdmin.list_filter
    list_editable = ['order', 'url', 'icon', ]
    search_fields = ['url', ]


@admin.register(models.CourseCoupons)
class CourseCouponsAdmin(AbstractAdmin):
    resource_class = create_resource(models.CourseCoupons)
    list_display = ['id', 'order', 'course_name', 'course_url', 'coupon_code', 'original_price', 'discount_price',
                    'start_date', 'expiration_date', 'is_active', 'updated_at', 'created_at', ]
    list_filter = AbstractAdmin.list_filter + ('is_active',)
    list_editable = ['order', 'course_name', 'course_url', 'coupon_code', 'original_price', 'discount_price',
                     'start_date', 'expiration_date', 'is_active', ]
    search_fields = ['course_name', 'course_url', 'coupon_code', ]
