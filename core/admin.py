from datetime import datetime
from django.contrib import admin
from django.conf import settings
from django.utils import timezone
from import_export.admin import ImportExportModelAdmin
from core.models import *
from django.contrib import messages
from django.db.models import Q


# Register your models here.


def delete_all(modeladmin, request, queryset):
    modeladmin.model.objects.all().delete()
    messages.success(request, 'All data deleted successfully.')


delete_all.short_description = 'Delete all data. Be careful, there is no warning yet!'


@admin.register(GeneralSetting)
class GeneralSettingAdmin(ImportExportModelAdmin):
    list_display = ['id', 'name', 'description', 'parameter', 'updated_at', 'created_at', ]
    search_fields = ['name', 'description', 'parameter', ]
    list_editable = ['description', 'parameter', ]

    class Meta:
        model = GeneralSetting


@admin.register(ImageSetting)
class ImageSettingAdmin(ImportExportModelAdmin):
    list_display = ['id', 'name', 'description', 'file', 'updated_at', 'created_at', ]
    search_fields = ['name', 'description', 'file', ]
    list_editable = ['description', 'file', ]

    class Meta:
        model = ImageSetting


@admin.register(Message)
class MessageAdmin(ImportExportModelAdmin):
    list_display = ['name', 'email', 'subject', 'message', 'success', 'error_message', 'updated_at', 'created_at', ]
    search_fields = ['name', 'email', 'subject', 'message', ]
    list_filter = ['success', 'error_message', ]

    class Meta:
        model = Message


@admin.register(Document)
class DocumentAdmin(ImportExportModelAdmin):
    list_display = ['id', 'name', 'button_text', 'file', 'show_on_page', 'updated_at', 'created_at', ]
    search_fields = ['name', 'button_text', ]
    list_editable = ['name', 'button_text', 'file', 'show_on_page', ]
    list_filter = ['show_on_page', ]

    class Meta:
        model = Document


@admin.register(Statistics)
class StatisticsAdmin(ImportExportModelAdmin):
    list_display = ['statistic_type', 'action', 'source', 'ip_address', 'user_agent', 'updated_at', 'created_at', ]
    search_fields = ['statistic_type', 'action', 'source', 'ip_address', 'user_agent', ]
    list_editable = []
    list_filter = ['statistic_type', 'action', 'source', ]

    class Meta:
        model = Statistics


@admin.action(description='Block user and IP address')
def block_user(modeladmin, request, queryset):
    blocked_users = BlockedUser.objects.filter(
        created_at__gte=datetime.fromtimestamp(timezone.now().timestamp() - settings.BLOCKED_USER_DURATION)
    )
    for item in queryset:
        if item.user:
            filtered_users = blocked_users.filter(Q(user=item.user) | Q(ip_address=item.user.ip_address))
        else:
            filtered_users = blocked_users.filter(ip_address=item.ip_address)

        if not filtered_users.exists():
            BlockedUser.objects.create(
                ip_address=item.ip_address,
                user=item.user,
            )
            messages.success(request, f'User is blocked. IP address: {item.ip_address} User: {item.user}')

    messages.success(request, f'{queryset.count()} items are updated.')


@admin.register(ActionLog)
class ActionLogAdmin(ImportExportModelAdmin):
    list_display = (
        'user', 'action', 'success', 'method', 'short_data', 'short_get_params', 'message', 'platform', 'browser',
        'ip_address', 'short_user_agent', 'is_deleted', 'updated_at', 'created_at',)
    list_editable = ()
    list_filter = ('is_deleted', 'success', 'method', 'action', 'platform', 'browser', 'platform',)
    search_fields = ('user__email', 'user__first_name', 'user__last_name', 'message', 'data',
                     'user_agent', 'get_params', 'ip_address',)
    autocomplete_fields = ('user',)

    actions = (block_user,)

    class Meta:
        model = ActionLog


@admin.register(BlockedUser)
class BlockedUserAdmin(ImportExportModelAdmin):
    list_display = ('id', 'user', 'ip_address', 'is_deleted', 'updated_at', 'created_at',)
    list_filter = ('is_deleted',)
    list_editable = ()
    search_fields = ('user__email', 'user__first_name', 'user__last_name', 'ip_address',)
    autocomplete_fields = ('user',)
