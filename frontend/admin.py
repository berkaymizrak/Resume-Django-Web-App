from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from frontend.models import *
from frontend import forms


# Register your models here.


@admin.register(Skill)
class SkillAdmin(ImportExportModelAdmin):
    form = forms.SkillAdminForm

    list_display = ['id', 'order', 'name', 'percent', 'skill_type', 'updated_at', 'created_at', ]
    search_fields = ['name', ]
    list_editable = ['order', 'name', 'percent', 'skill_type', ]

    class Meta:
        model = Skill


@admin.register(SkillTypes)
class SkillTypesAdmin(ImportExportModelAdmin):
    list_display = ['id', 'name', 'updated_at', 'created_at', ]
    search_fields = ['name', ]
    list_editable = ['name', ]

    class Meta:
        model = SkillTypes


@admin.register(SocialMedia)
class SocialMediaAdmin(ImportExportModelAdmin):
    list_display = ['id', 'order', 'url', 'icon', 'updated_at', 'created_at', ]
    search_fields = ['url', ]
    list_editable = ['order', 'url', 'icon', ]

    class Meta:
        model = SocialMedia


@admin.register(CourseCoupons)
class CourseCouponsAdmin(ImportExportModelAdmin):
    list_display = ['id', 'order', 'course_name', 'course_url', 'coupon_code', 'original_price', 'discount_price',
                    'start_date', 'expiration_date', 'is_active', 'updated_at', 'created_at', ]
    search_fields = ['course_name', 'course_url', 'coupon_code', ]
    list_editable = ['order', 'course_name', 'course_url', 'coupon_code', 'original_price', 'discount_price',
                     'start_date', 'expiration_date', 'is_active', ]
    list_filter = ['is_active', ]

    class Meta:
        model = CourseCoupons
