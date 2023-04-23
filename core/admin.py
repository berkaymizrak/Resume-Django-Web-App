from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from core.models import *


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
class RedirectSlugAdmin(ImportExportModelAdmin):
    list_display = ['id', 'slug', 'new_url', 'updated_date', 'created_date', ]
    search_fields = ['slug', 'new_url', ]
    list_editable = ['slug', 'new_url', ]
    list_filter = []

    class Meta:
        model = RedirectSlug


@admin.register(Statistics)
class StatisticsAdmin(ImportExportModelAdmin):
    list_display = ['statistic_type', 'action', 'source', 'ip_address', 'user_agent', 'updated_date', 'created_date', ]
    search_fields = ['statistic_type', 'action', 'source', 'ip_address', 'user_agent', ]
    list_editable = []
    list_filter = ['statistic_type', 'action', 'source', ]

    class Meta:
        model = Statistics
