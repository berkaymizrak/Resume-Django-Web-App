from django.shortcuts import redirect
from user.models import *

# from django.contrib import messages
# from django.utils.safestring import mark_safe

def login_required_redirect(function):
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated:
            return function(request, *args, **kwargs)
        else:
            return redirect('index')
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap

def logout_required(function):
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('index')
        else:
            return function(request, *args, **kwargs)
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap



