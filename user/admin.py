from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from user.models import *
from user import forms


# Register your models here.


@admin.register(GeneralSetting)
class GeneralSettingAdmin(ImportExportModelAdmin):
    list_display = ['id', 'name', 'description', 'parameter', 'updated_date', 'created_date', ]
    search_fields = ['name', 'description', 'parameter', ]
    list_editable = ['description', 'parameter', ]

    class Meta:
        model = GeneralSetting


@admin.register(ImageSetting)
class ImageSettingAdmin(ImportExportModelAdmin):
    list_display = ['id', 'name', 'description', 'file', 'updated_date', 'created_date', ]
    search_fields = ['name', 'description', 'file', ]
    list_editable = ['description', 'file', ]

    class Meta:
        model = ImageSetting


@admin.register(Skill)
class SkillAdmin(ImportExportModelAdmin):
    form = forms.SkillAdminForm

    list_display = ['id', 'order', 'name', 'percent', 'skill_type', 'updated_date', 'created_date', ]
    search_fields = ['name', ]
    list_editable = ['order', 'name', 'percent', 'skill_type', ]

    class Meta:
        model = Skill


@admin.register(SkillTypes)
class SkillTypesAdmin(ImportExportModelAdmin):
    list_display = ['id', 'name', 'updated_date', 'created_date', ]
    search_fields = ['name', ]
    list_editable = ['name', ]

    class Meta:
        model = SkillTypes


@admin.register(SocialMedia)
class SocialMediaAdmin(ImportExportModelAdmin):
    list_display = ['id', 'order', 'url', 'icon', 'updated_date', 'created_date', ]
    search_fields = ['url', ]
    list_editable = ['order', 'url', 'icon', ]

    class Meta:
        model = SocialMedia


@admin.register(Message)
class MessageAdmin(ImportExportModelAdmin):
    list_display = ['name', 'email', 'subject', 'message', 'success', 'error_message', 'updated_date', 'created_date', ]
    search_fields = ['name', 'email', 'subject', 'message', ]
    list_filter = ['success', 'error_message', ]

    class Meta:
        model = Message


@admin.register(Document)
class DocumentAdmin(ImportExportModelAdmin):
    list_display = ['id', 'name', 'button_text', 'file', 'show_on_page', 'updated_date', 'created_date', ]
    search_fields = ['name', 'button_text', ]
    list_editable = ['name', 'button_text', 'file', 'show_on_page', ]
    list_filter = ['show_on_page', ]

    class Meta:
        model = Document


@admin.register(RedirectSlug)
class DocumentAdmin(ImportExportModelAdmin):
    list_display = ['id', 'slug', 'new_url', 'updated_date', 'created_date', ]
    search_fields = ['slug', 'new_url', ]
    list_editable = ['slug', 'new_url', ]
    list_filter = []

    class Meta:
        model = RedirectSlug


@admin.register(CourseCoupons)
class CourseCouponsAdmin(ImportExportModelAdmin):
    list_display = ['id', 'order', 'course_name', 'course_url', 'coupon_code', 'original_price', 'discount_price',
                    'expiration_date', 'is_active', 'updated_date', 'created_date', ]
    search_fields = ['course_name', 'course_url', 'coupon_code', ]
    list_editable = ['order', 'course_name', 'course_url', 'coupon_code', 'original_price', 'discount_price',
                     'expiration_date', 'is_active', ]
    list_filter = ['is_active', ]

    class Meta:
        model = CourseCoupons


@admin.register(Statistics)
class StatisticsAdmin(ImportExportModelAdmin):
    list_display = ['statistic_type', 'action', 'source', 'ip_address', 'user_agent', 'updated_date', 'created_date', ]
    search_fields = ['statistic_type', 'action', 'source', 'ip_address', 'user_agent', ]
    list_editable = []
    list_filter = ['statistic_type', 'action', 'source', ]

    class Meta:
        model = Statistics
