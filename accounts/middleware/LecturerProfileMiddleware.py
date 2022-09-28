from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse

from accounts.models import LecturerProfile


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
            while request.path not in list([reverse('admin:login'), reverse('login'), reverse('register_user')]):
                return utilityfunc(request.path)
        return response

    return middleware


def utilityfunc(path):
    if path == reverse('login'):
        return redirect('login')
    elif path == reverse('register_user'):
        return redirect('register_user')
    elif path == reverse('admin:login'):
        return redirect('admin:login')
    else:
        return redirect('login')