from django.contrib import messages
from django.urls import reverse
from django.shortcuts import redirect

from ratelimit.decorators import ratelimit


def login_wrapper(login_func):

    @ratelimit(method='POST', key='post:username', rate='2/20m')
    def admin_login(request, **kwargs):
        if not getattr(request, 'limited', False):
            return login_func(request, **kwargs)
        messages.error(request, 'Too many login attempts, please try again in 20 minutes')
        return redirect(reverse("admin:index"))

    return admin_login
