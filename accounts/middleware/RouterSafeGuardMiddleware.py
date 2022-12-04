from django.shortcuts import redirect, get_object_or_404, render
from django.urls import reverse, resolve, path
import re
from django.http import HttpResponse

from accounts.middleware.whitelisted_routes import whitelisted_urls


# from dashboard.views import runurl


class RouterMiddleware:
    def __init__(self, get_response):
        # self.whitelisted_urls = '/dashboard/factual/limiting/(?P<token>[^/]+)\\Z'
        self.whitelisted_urls = '/accounts/confirm-email/(?P<token>[^/]+)\\Z'

        self.get_response = get_response

    def __call__(self, request):
        exception_urls = list(EXCEPTION_URL_LIST)
        response = self.get_response(request)
        if not request.user.is_authenticated:
            if request.path not in exception_urls:
                return self.utilityfunc(request, response)
        return response

    def utilityfunc(self, request, rpath):
        exception_urls = list(whitelisted_urls(request))
        if rpath in exception_urls:
            return redirect(rpath)
        else:
            return redirect('welcome')

    def utilityfunc_wl(self, rpath):
        return redirect(rpath)