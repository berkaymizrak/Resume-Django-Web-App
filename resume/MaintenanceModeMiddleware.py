from core.utils import create_action_log
from django.shortcuts import redirect
from django.core.exceptions import MiddlewareNotUsed
from django.conf import settings
from django.urls import reverse


class MaintenanceModeMiddleware(object):
    """Middleware that redirects to a maintenance page if the site is in maintenance mode."""

    def __init__(self, get_response):
        self.get_response = get_response
        if settings.DEBUG or not settings.SITE_DOMAIN:
            raise MiddlewareNotUsed
        if not settings.MAINTENANCE_MODE:
            raise MiddlewareNotUsed

    def __call__(self, request):
        """If the request domain is not the canonical domain, redirect."""
        hostname = request.get_host().split(':', 1)[0]
        # Don't perform redirection for testing or local development.
        if hostname in ('localhost', '127.0.0.1', '0.0.0.0'):
            return self.get_response(request)

        if request.path_info == '/favicon.ico/' or request.path_info == '/favicon.ico':
            return self.get_response(request)

        if request.user.is_superuser:
            return self.get_response(request)

        if request.path_info.startswith('/api/'):
            return self.get_response(request)

        if request.path_info.startswith('/admin/'):
            return self.get_response(request)

        if settings.MAINTENANCE_MODE and request.path_info != reverse('maintenance'):
            create_action_log(request, 'maintenance_on_redirected', True)
            return redirect('maintenance', permanent=True)

        return self.get_response(request)
