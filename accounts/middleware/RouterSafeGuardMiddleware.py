from django.shortcuts import redirect
from django.urls import reverse

from accounts.middleware.whitelisted_routes import whitelisted_urls


def utilityfunc(request, rpath):
    exception_urls = whitelisted_urls(request)
    if rpath in exception_urls:
        return redirect(rpath)
    else:
        return redirect('welcome')


def utilityfunc_wl(rpath):
    return redirect(rpath)


class RouterMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated:
            return redirect('welcome')

        response = self.get_response(request)

        if request.path in whitelisted_urls(request):
            return response





    def process_view(self, request, view_func, view_args, view_kwargs):
        whitelist = [
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
                    kwargs={'uidb64': view_kwargs.get('uidb64'),
                            'token': view_kwargs.get('token')}),
        ]

        if request.path in whitelist:
            return utilityfunc(request, request.path)

        return None