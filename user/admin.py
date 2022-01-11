from django.contrib import admin

from user.models import *

# Register your models here.


@admin.register(GeneralSetting)
class GeneralSettingAdmin(admin.ModelAdmin):

    list_display = ['id', 'setting', 'description', 'parameter', 'date']
    search_fields = ['setting', 'description', 'parameter', ]
    list_editable = ['parameter', ]
    # list_filter = ['sebep', 'user']

    class Meta:
        model = GeneralSetting


@admin.register(ImageSetting)
class ImageSettingAdmin(admin.ModelAdmin):

    list_display = ['id', 'setting', 'description', 'file', 'date']
    search_fields = ['setting', 'description', 'file', ]
    list_editable = ['file', ]
    # list_filter = ['sebep', 'user']

    class Meta:
        model = ImageSetting


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):

    list_display = ['id', 'order', 'header', 'percent', 'date']
    search_fields = ['header', ]
    list_editable = ['order', 'header', 'percent', ]
    # list_filter = ['header', ]

    class Meta:
        model = Skill


@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):

    list_display = ['id', 'order', 'header', 'icon', 'date']
    search_fields = ['header', ]
    list_editable = ['order', 'header', 'icon', ]
    # list_filter = ['header', ]

    class Meta:
        model = Feature


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):

    list_display = ['name', 'email', 'message', 'success', 'error_message', 'date']
    search_fields = ['name', 'email', 'message', ]
    # list_editable = ['success', 'error_message', 'icon', ]
    list_filter = ['success', 'error_message', ]

    class Meta:
        model = Message


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ['id', 'button_text', 'file', 'date']
    search_fields = ['button_text', 'file', ]
    list_editable = ['button_text', 'file', ]

    list_filter = ['button_text']

    class Meta:
        model = Document

