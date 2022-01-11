from django.conf import settings
from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect, reverse


class ParameterMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        """
        Intro popup will be shown only once.
        'show_intro' key in session will be checked in views.py and will be sent to frontend.
        Javascript function will check show_intro to show popup or not.
        """
        intro = request.GET.get('intro', None)
        if intro:
            request.session['show_intro'] = False
            request.session['redirected'] = True
            return redirect(reverse(view_func))
        else:
            redirected = request.session.get('redirected', None)
            if redirected:
                request.session['redirected'] = False
            else:
                request.session['show_intro'] = True
            return None

