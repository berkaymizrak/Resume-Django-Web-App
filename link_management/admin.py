from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from link_management.models import *

# Register your models here.


@admin.register(RedirectSlug)
class RedirectSlugAdmin(ImportExportModelAdmin):
    list_display = ['id', 'slug', 'new_url', 'updated_at', 'created_at', ]
    search_fields = ['slug', 'new_url', ]
    list_editable = ['slug', 'new_url', ]
    list_filter = []

    class Meta:
        model = RedirectSlug
