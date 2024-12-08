from datetime import datetime
from django.contrib import admin
from django.conf import settings
from django.utils import timezone
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from core import models
from django.contrib import messages
from django.db.models import Q


# Register your models here.


@admin.action(description='Toggle is_active - Custom Action!')
def toggle_is_active(modeladmin, request, queryset):
    for item in queryset:
        item.is_active = not item.is_active
        item.save()

    messages.success(request, f'{queryset.count()} öğe güncellendi.')


@admin.action(description='Toggle is_deleted - Custom Action!')
def toggle_is_deleted(modeladmin, request, queryset):
    for item in queryset:
        item.is_deleted = not item.is_deleted
        item.save()

    messages.success(request, f'{queryset.count()} öğe güncellendi.')


@admin.action(description='Seçilenleri Sil - Custom Action!')
def silent_delete(modeladmin, request, queryset):
    queryset.delete()


def create_resource(django_model, django_fields=None, django_exclude=None):
    class model_resource(resources.ModelResource):
        class Meta:
            model = django_model
            if django_fields:
                fields = ('id',) + django_fields
            # else is all fields
            # exclude = (
            #     'is_deleted',
            #     'updated_at',
            #     'created_at',
            # )
            exclude = django_exclude if django_exclude else ()

    return model_resource


class AbstractAdmin(ImportExportModelAdmin):
    list_filter = ('is_deleted',)
    actions = (toggle_is_deleted, silent_delete,)

    def get_queryset(self, request):
        if request.user.is_superuser:
            return self.model.objects.all()
        else:
            return self.model.objects.filter(is_deleted=False)


@admin.register(models.GeneralSetting)
class GeneralSettingAdmin(AbstractAdmin):
    resource_class = create_resource(models.GeneralSetting)
    list_display = ['id', 'name', 'description', 'parameter', 'updated_at', 'created_at', ]
    list_filter = AbstractAdmin.list_filter
    list_editable = ['description', 'parameter', ]
    search_fields = ['name', 'description', 'parameter', ]


@admin.register(models.ImageSetting)
class ImageSettingAdmin(AbstractAdmin):
    resource_class = create_resource(models.ImageSetting)
    list_display = ['id', 'name', 'description', 'file', 'updated_at', 'created_at', ]
    list_filter = AbstractAdmin.list_filter
    list_editable = ['description', 'file', ]
    search_fields = ['name', 'description', 'file', ]


@admin.register(models.Message)
class MessageAdmin(AbstractAdmin):
    resource_class = create_resource(models.Message)
    list_display = ['name', 'email', 'subject', 'message', 'success', 'error_message', 'updated_at', 'created_at', ]
    list_filter = AbstractAdmin.list_filter + ('success', 'error_message',)
    list_editable = ()
    search_fields = ['name', 'email', 'subject', 'message', ]


@admin.register(models.Document)
class DocumentAdmin(AbstractAdmin):
    resource_class = create_resource(models.Document)
    list_display = ['id', 'name', 'button_text', 'file', 'show_on_page', 'updated_at', 'created_at', ]
    list_filter = AbstractAdmin.list_filter + ('show_on_page',)
    list_editable = ['name', 'button_text', 'file', 'show_on_page', ]
    search_fields = ['name', 'button_text', ]


@admin.register(models.Statistics)
class StatisticsAdmin(AbstractAdmin):
    resource_class = create_resource(models.Statistics)
    list_display = ['statistic_type', 'action', 'source', 'ip_address', 'user_agent', 'updated_at', 'created_at', ]
    list_filter = AbstractAdmin.list_filter + ('statistic_type', 'action', 'source',)
    list_editable = []
    search_fields = ['statistic_type', 'action', 'source', 'ip_address', 'user_agent', ]


@admin.action(description='Block user and IP address')
def block_user(modeladmin, request, queryset):
    blocked_users = models.BlockedUser.objects.filter(
        Q(created_at__gte=datetime.fromtimestamp(timezone.now().timestamp() - settings.BLOCKED_USER_DURATION))
        | Q(permanent=True)
    )
    for item in queryset:
        if item.user:
            filtered_users = blocked_users.filter(Q(user=item.user) | Q(ip_address=item.ip_address))
        else:
            filtered_users = blocked_users.filter(ip_address=item.ip_address)

        if not filtered_users.exists():
            models.BlockedUser.objects.create(
                ip_address=item.ip_address,
                user=item.user,
                # phone=item.user.phone if item.user else '',
                permanent=False,
            )
            messages.success(request, f'User is blocked. IP address: {item.ip_address} User: {item.user}')

    messages.success(request, f'{queryset.count()} öğe güncellendi.')


@admin.action(description='Permanent block user and IP address')
def permanent_block_user(modeladmin, request, queryset):
    blocked_users = models.BlockedUser.objects.filter(
        Q(created_at__gte=datetime.fromtimestamp(timezone.now().timestamp() - settings.BLOCKED_USER_DURATION))
        | Q(permanent=True)
    )
    for item in queryset:
        if item.user:
            filtered_users = blocked_users.filter(Q(user=item.user) | Q(ip_address=item.ip_address))
        else:
            filtered_users = blocked_users.filter(ip_address=item.ip_address)

        if not filtered_users.exists():
            models.BlockedUser.objects.create(
                ip_address=item.ip_address,
                user=item.user,
                # phone=item.user.phone if item.user else '',
                permanent=True,
            )
            messages.success(request, f'User is permanently blocked. IP address: {item.ip_address} User: {item.user}')
        else:
            for blocked_user in filtered_users:
                if not blocked_user.permanent:
                    blocked_user.permanent = True
                    blocked_user.save()
                    messages.success(request,
                                     f'User is permanently blocked. IP address: {item.ip_address} User: {item.user}')

    messages.success(request, f'{queryset.count()} öğe güncellendi.')


@admin.action(description='Permanent block ONLY IP address')
def permanent_block_ip_address(modeladmin, request, queryset):
    blocked_users = models.BlockedUser.objects.filter(
        Q(created_at__gte=datetime.fromtimestamp(timezone.now().timestamp() - settings.BLOCKED_USER_DURATION))
        | Q(permanent=True)
    )
    for item in queryset:
        filtered_users = blocked_users.filter(ip_address=item.ip_address, permanent=True)

        if not filtered_users.exists():
            models.BlockedUser.objects.create(
                ip_address=item.ip_address,
                user=item.user,
                # phone=item.user.phone if item.user else '',
                permanent=True,
            )
            messages.success(request, f'IP address is permanently blocked. IP address: {item.ip_address}')
        else:
            for blocked_user in filtered_users:
                if not blocked_user.permanent:
                    blocked_user.permanent = True
                    blocked_user.save()
                    messages.success(request,
                                     f'IP address is permanently blocked. IP address: {item.ip_address} User: {item.user}')

    messages.success(request, f'{queryset.count()} öğe güncellendi.')


def generate_unique_uuids(modeladmin, request, queryset):
    from core.tasks import generate_unique_uuids_task
    generate_unique_uuids_task.delay()


@admin.register(models.ActionLog)
class ActionLogAdmin(AbstractAdmin):
    resource_class = create_resource(models.ActionLog)
    list_display = ('created_at', 'user', 'action', 'success', 'path',
                    'method', 'ip_address', 'unique_key', 'short_data', 'short_get_params',
                    'message', 'platform', 'browser', 'short_user_agent', 'is_deleted', 'updated_at',)
    list_filter = AbstractAdmin.list_filter + ('success', 'method', 'action', 'platform', 'browser', 'platform',)
    list_editable = ()
    search_fields = ('user__email', 'user__first_name', 'user__last_name', 'message', 'data',
                     'user_agent', 'get_params', 'ip_address', 'unique_key', 'path',)
    autocomplete_fields = ('user',)

    actions = AbstractAdmin.actions + (
        generate_unique_uuids,
        block_user, permanent_block_user, permanent_block_ip_address,
    )


@admin.action(description='Toggle permanent')
def toggle_permanent(modeladmin, request, queryset):
    for item in queryset:
        item.permanent = not item.permanent
        item.save()

    messages.success(request, f'{queryset.count()} öğe güncellendi.')


@admin.register(models.BlockedUser)
class BlockedUserAdmin(AbstractAdmin):
    resource_class = create_resource(models.BlockedUser)
    list_display = ('created_at', 'user', 'ip_address', 'phone', 'permanent', 'is_deleted', 'updated_at',)
    list_filter = AbstractAdmin.list_filter + ('permanent',)
    list_editable = ()
    search_fields = ('user__email', 'user__first_name', 'user__last_name', 'phone', 'ip_address',)
    autocomplete_fields = ('user',)

    actions = AbstractAdmin.actions + (toggle_permanent,)
