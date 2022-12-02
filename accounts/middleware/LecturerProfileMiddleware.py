from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse

from accounts.models import LecturerProfile

exception_urls_ = [reverse('admin:login'),
                   reverse('welcome'),
                   reverse('password_reset_request'),
                   reverse('password_reset_done'),
                   reverse('password_reset_confirm'),
                   reverse('password_reset_complete'),
                   reverse('login'),
                   reverse('register_user'),
                   '/accounts/reset/Mzkz/(?P<token>[^/]+)\\Z'
                   ]

def lpm(get_response):
    def middleware(request):
        response = get_response(request)
        try:
            if request.user.id is not None and request.user.is_lecturer is True:
                LecturerProfile.objects.filter(user=request.user).get()
        except LecturerProfile.DoesNotExist:
            while not (request.path == reverse('setup-lecturer-profile', kwargs={'user_id': request.user.id})):
                return redirect(reverse('setup-lecturer-profile', kwargs={'user_id': request.user.id}))
        return response

    return middleware


def check_authenticated_user(get_response):
    def middleware(request):
        response = get_response(request)
        if request.user.id is None:
            while request.path not in list(exception_urls_):
                return utilityfunc(request.path)
        return response

    return middleware


def utilityfunc(path):
    if path == reverse('login'):
        return redirect('login')
    elif path == reverse('register_user'):
        return redirect('register_user')
    elif path == reverse('welcome'):
        return redirect('welcome')
    elif path == reverse('password_reset_request'):
        return redirect('password_reset_request')
    elif path == reverse('password_reset_done'):
        return redirect('password_reset_done')
    elif path == reverse('password_reset_confirm'):
        return redirect('password_reset_confirm')
    elif path == reverse('password_reset_complete'):
        return redirect('password_reset_complete')
    elif path == r'/accounts/reset/Mzkz/(?P<token>[^/]+)\\Z':
        return r'/accounts/reset/Mzkz/(?P<token>[^/]+)\\Z'
    elif path == reverse('admin:login'):
        return redirect('admin:login')
    else:
        return redirect('welcome')