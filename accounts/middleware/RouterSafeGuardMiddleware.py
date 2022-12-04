from django.shortcuts import redirect, get_object_or_404, render
from django.urls import reverse, resolve, path
import re
from django.http import HttpResponse


# from dashboard.views import runurl


class RouterMiddleware:
    def __init__(self, get_response):
        # self.whitelisted_urls = '/dashboard/factual/limiting/(?P<token>[^/]+)\\Z'
        self.whitelisted_urls = '/accounts/confirm-email/(?P<token>[^/]+)\\Z'


        self.get_response = get_response

    def __call__(self, request):
        exception_urls = list([
            reverse('admin:login'),
            reverse('welcome'),
            reverse('password_reset_request'),
            reverse('password_reset_done'),
            reverse('password_reset_complete'),
            reverse('login_student'),
            reverse('login_lecturer'),
            reverse('login_administrator'),
            reverse('register_student'),
            reverse('register_lecturer'),
            reverse('password_reset_request'),
            reverse('password_reset_done'),
            reverse('password_reset_complete'),
            reverse('password_reset_confirm',
                    kwargs={'uidb64': request.GET.get('uidb64'),
                            'token': request.GET.get('token')}),
        ])
        response = self.get_response(request)
        if not request.user.is_authenticated:
            if request.path not in exception_urls:
                return self.utilityfunc(request,response)
        return response

    def utilityfunc(self, request, rpath):
        exception_urls = list([
            reverse('admin:login'),
            reverse('welcome'),
            reverse('password_reset_request'),
            reverse('password_reset_done'),
            reverse('password_reset_complete'),
            reverse('login_student'),
            reverse('login_lecturer'),
            reverse('login_administrator'),
            reverse('register_student'),
            reverse('register_lecturer'),
            reverse('password_reset_request'),
            reverse('password_reset_done'),
            reverse('password_reset_complete'),
            reverse('password_reset_confirm',
                    kwargs={'uidb64': request.GET.get('uidb64'),
                            'token': request.GET.get('token')}),
        ])
        if rpath in exception_urls:
            return redirect(rpath)
        else:
            return redirect('welcome')

    def utilityfunc_wl(self, rpath):
        return redirect(rpath)