from core.admin import delete_all
from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from program.models import *


# Register your models here.


@admin.register(ExternalProgram)
class ExternalProgramAdmin(ImportExportModelAdmin):
    list_display = ['id', 'name', 'description', 'parameter', 'updated_at', 'created_at', ]
    search_fields = ['name', 'description', 'parameter', ]
    list_editable = ['description', 'parameter', ]

    class Meta:
        model = ExternalProgram


@admin.register(ExternalLogs)
class ExternalLogsAdmin(admin.ModelAdmin):
    list_display = ['name', 'program', 'success', 'parameter', 'ip_address', 'updated_at', 'created_at', ]
    search_fields = ['name', 'parameter', 'program', 'ip_address', ]
    list_filter = ['success', 'name', 'program', 'ip_address', ]

    actions = [delete_all]

    class Meta:
        model = ExternalLogs
