from datetime import datetime
from django.utils import timezone
from core.models import ActionLog, BlockedUser
from core.utils import get_client_ip, create_action_log
from django.core.exceptions import MiddlewareNotUsed
from django.conf import settings
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.urls import reverse


class SecurityMiddleware(object):
    """Middleware that redirects to a maintenance page if the site is in maintenance mode."""

    def __init__(self, get_response):
        self.get_response = get_response
        if settings.DEBUG:
            raise MiddlewareNotUsed

    def __call__(self, request):
        """If the request domain is not the canonical domain, redirect."""

        if request.user.is_superuser or request.user.is_staff:
            return self.get_response(request)

        if request.path_info == reverse('csrf_failure'):
            return self.get_response(request)

        action_logs = ActionLog.objects.filter(ip_address=get_client_ip(request))

        blocked_users = BlockedUser.objects.filter(
            created_at__gte=datetime.fromtimestamp(timezone.now().timestamp() - settings.BLOCKED_USER_DURATION)
        )
        if request.user.is_authenticated:
            blocked_users = blocked_users.filter(Q(user=request.user) | Q(ip_address=get_client_ip(request)))
        else:
            blocked_users = blocked_users.filter(ip_address=get_client_ip(request))

        for limitation in settings.BLOCK_LIMITS:
            if action_logs.filter(
                    created_at__gte=datetime.fromtimestamp(timezone.now().timestamp() - limitation.get('duration', 60)),
                    **limitation.get('filters', {}),
            ).count() >= limitation.get('limit', 1000):
                if not blocked_users.exists():
                    BlockedUser.objects.create(
                        ip_address=get_client_ip(request),
                        user=request.user if request.user.is_authenticated else None,
                    )
                create_action_log(request, 'blocked', False, 'Blocked by action log limit.')
                return HttpResponseRedirect(reverse('csrf_failure'))

        if blocked_users.exists():
            return HttpResponseRedirect(reverse('csrf_failure'))

        return self.get_response(request)
