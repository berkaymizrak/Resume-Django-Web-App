from datetime import datetime
from django.utils import timezone
from core.models import ActionLog, BlockedUser
from core.utils import get_client_ip, create_action_log
from django.core.exceptions import MiddlewareNotUsed
from django.conf import settings
from django.db.models import Q
from django.shortcuts import redirect
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

        action_logs = ActionLog.objects.filter(ip_address=get_client_ip(request))

        blocked_users = BlockedUser.objects.filter(
            Q(created_at__gte=datetime.fromtimestamp(timezone.now().timestamp() - settings.BLOCKED_USER_DURATION))
            | Q(permanent=True)
        )
        if request.user.is_authenticated:
            blocked_users = blocked_users.filter(Q(user=request.user) | Q(ip_address=get_client_ip(request)))
        else:
            blocked_users = blocked_users.filter(ip_address=get_client_ip(request))

        if request.path_info == reverse('blocked_user'):
            if blocked_users.exists():
                blocked_user = blocked_users.first()
                if blocked_user.permanent:
                    blocked_users = blocked_users.filter(ip_address=get_client_ip(request))
                    if not blocked_users.exists():
                        BlockedUser.objects.create(
                            ip_address=get_client_ip(request),
                            user=blocked_user.user if blocked_user.user else request.user if request.user.is_authenticated else None,
                            phone=request.user.phone if request.user.is_authenticated else '',
                            permanent=True,
                        )
                return self.get_response(request)
            else:
                return redirect('landing', permanent=True)

        for limitation in settings.BLOCK_LIMITS:
            if action_logs.filter(
                    created_at__gte=datetime.fromtimestamp(
                        timezone.now().timestamp() - limitation.get('duration', 60 * 60)
                    ),
                    **limitation.get('filters', {}),
            ).count() >= limitation.get('limit', 1000):
                if not blocked_users.exists():
                    BlockedUser.objects.create(
                        ip_address=get_client_ip(request),
                        user=request.user if request.user.is_authenticated else None,
                        phone=request.user.phone if request.user.is_authenticated else '',
                        permanent=False,
                    )
                    plain_message = 'Eylem limiti tarafından engellendi.' \
                                    f'\nIP: {get_client_ip(request)}' \
                                    f'\nKullanıcı: {request.user if request.user.is_authenticated else None}' \
                                    f'\nLimitation: {limitation}'
                    # send_email_alerts(
                    #     mail_subject='Kullanıcı Engellendi',
                    #     plain_message=plain_message,
                    # )
                    from core.tasks import send_slack_notification
                    summary_message = f'Kullanıcı Engellendi. IP: {get_client_ip(request)}'
                    send_slack_notification.delay(
                        '#berkay-mizrak',
                        f'Kullanıcı Engellendi - {get_client_ip(request)}',
                        plain_message,
                        summary_message,
                    )
                create_action_log(request, 'blocked_user', False, 'Blocked by action log limit.', data=limitation)
                return redirect('blocked_user', permanent=True)

        if blocked_users.exists():
            return redirect('blocked_user', permanent=True)

        return self.get_response(request)
