from core.admin import AbstractAdmin, create_resource
from django.contrib import admin
from program import models


# Register your models here.


@admin.register(models.ExternalProgram)
class ExternalProgramAdmin(AbstractAdmin):
    resource_class = create_resource(models.ExternalProgram)
    list_display = ['id', 'name', 'description', 'parameter', 'updated_at', 'created_at', ]
    list_filter = AbstractAdmin.list_filter
    list_editable = ['description', 'parameter', ]
    search_fields = ['name', 'description', 'parameter', ]


@admin.register(models.ExternalLogs)
class ExternalLogsAdmin(AbstractAdmin):
    resource_class = create_resource(models.ExternalLogs)
    list_display = ['name', 'program', 'success', 'parameter', 'ip_address', 'updated_at', 'created_at', ]
    list_filter = AbstractAdmin.list_filter + ('success', 'name', 'program', 'ip_address',)
    list_editable = []
    search_fields = ['name', 'parameter', 'program', 'ip_address', ]
