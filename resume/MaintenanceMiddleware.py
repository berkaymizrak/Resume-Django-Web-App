from django.conf import settings
from django.http import HttpResponse
from django.template import loader
from django.utils.deprecation import MiddlewareMixin


class MaintenanceMiddleware(MiddlewareMixin):

    def process_view(self, request, view_func, view_args, view_kwargs):
        if settings.UNDER_MAINTENANCE and not request.user.is_staff:
            return HttpResponse(loader.render_to_string('503.html'), status=503)