from django.contrib import admin

from user.models import *
from import_export.admin import ImportExportModelAdmin

# Register your models here.


@admin.register(GeneralSetting)
class GeneralSettingAdmin(ImportExportModelAdmin):

    list_display = ['id', 'name', 'description', 'parameter', 'date']
    search_fields = ['name', 'description', 'parameter', ]
    list_editable = ['parameter', ]
    # list_filter = ['sebep', 'user']

    class Meta:
        model = GeneralSetting


@admin.register(ImageSetting)
class ImageSettingAdmin(ImportExportModelAdmin):

    list_display = ['id', 'name', 'description', 'file', 'date']
    search_fields = ['name', 'description', 'file', ]
    list_editable = ['file', ]
    # list_filter = ['sebep', 'user']

    class Meta:
        model = ImageSetting


@admin.register(Skill)
class SkillAdmin(ImportExportModelAdmin):

    list_display = ['id', 'order', 'name', 'percent', 'date']
    search_fields = ['name', ]
    list_editable = ['order', 'name', 'percent', ]
    # list_filter = ['name', ]

    class Meta:
        model = Skill


@admin.register(SocialMedia)
class SocialMediaAdmin(ImportExportModelAdmin):

    list_display = ['id', 'order', 'url', 'icon', 'date']
    search_fields = ['url', ]
    list_editable = ['order', 'url', 'icon', ]
    # list_filter = ['name', ]

    class Meta:
        model = SocialMedia


@admin.register(Message)
class MessageAdmin(ImportExportModelAdmin):

    list_display = ['name', 'email', 'message', 'success', 'error_message', 'date']
    search_fields = ['name', 'email', 'message', ]
    # list_editable = ['success', 'error_message', 'icon', ]
    list_filter = ['success', 'error_message', ]

    class Meta:
        model = Message


@admin.register(Document)
class DocumentAdmin(ImportExportModelAdmin):
    list_display = ['id', 'button_text', 'file', 'date']
    search_fields = ['button_text', 'file', ]
    list_editable = ['button_text', 'file', ]

    list_filter = ['button_text']

    class Meta:
        model = Document

