from core.admin import AbstractAdmin, create_resource
from django.contrib import admin
from link_management import models


# Register your models here.


@admin.register(models.RedirectSlug)
class RedirectSlugAdmin(AbstractAdmin):
    resource_class = create_resource(models.RedirectSlug)
    list_display = ('id', 'slug', 'redirect_url', 'new_url', 'is_deleted', 'updated_at', 'created_at',)
    list_filter = AbstractAdmin.list_filter
    list_editable = ('slug', 'new_url',)
    search_fields = ('slug', 'new_url',)
    autocomplete_fields = ()
    readonly_fields = ('redirect_url',)
