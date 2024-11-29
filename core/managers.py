from django.db import models
from django.db.models import Q


class FilterManager(models.Manager):
    # def get_queryset(self):
    #     return self.is_not_deleted_filter()

    def admin_filter(self, queryset=None, filters=dict()):
        if queryset is None:
            queryset = super().get_queryset()

        return queryset.filter(**filters)

    def is_not_deleted_filter(self, queryset=None, filters=dict()):
        if queryset is None:
            queryset = super().get_queryset()

        if 'is_deleted' not in filters.keys():
            filters['is_deleted'] = False

        if hasattr(self.model, 'is_active'):
            filters['is_active'] = True

        return queryset.filter(**filters)

    def user_filter(self, queryset=None, user=None, filters=dict()):
        if queryset is None:
            queryset = super().get_queryset()

        if user is None:
            raise ValueError('User must be provided')
        else:
            # if user.is_authenticated and user.is_superuser is not True:
            if user.is_authenticated:
                queryset = queryset.filter(Q(user=user) | Q(user__isnull=True))
            else:
                queryset = queryset.filter(user__isnull=True)
            # if user.is_superuser:
            #     return self.admin_filter(queryset=queryset, filters=filters)
            # else:
            return self.is_not_deleted_filter(queryset=queryset, filters=filters)

    def guest_filter(self, user=None, filters=dict()):
        queryset = super().get_queryset()

        if user is not None:
            # if user.is_superuser:
            #     return self.admin_filter(queryset=queryset, filters=filters)

            if hasattr(self.model, 'user'):
                return self.user_filter(queryset=queryset, user=user, filters=filters)

        return self.is_not_deleted_filter(queryset=queryset, filters=filters)
