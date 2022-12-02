from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse

from accounts.middleware.LecturerProfileMiddleware import exception_urls_
from accounts.models import LecturerProfile, Student


def spm(get_response):
    def middleware(request):
        response = get_response(request)
        try:
            if request.user.id is not None and request.user.is_student is True and request.user.is_active is True:
                Student.objects.filter(user=request.user).get()
                # return redirect(reverse('login_student'))
        except Student.DoesNotExist:
            while not (request.path == reverse('student_profile_create', kwargs={'pk': request.user.id})):
                return redirect(reverse('student_profile_create', kwargs={'pk': request.user.id}))
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
    elif path == reverse('password_reset_complete'):
        return redirect('password_reset_complete')
    elif path == r"/accounts/reset/(?P<uidb64>[^/]+)\\Z')/(?P<token>[^/]+)\\Z":
        return redirect(r"/accounts/reset/(?P<uidb64>[^/]+)\\Z'/(?P<token>[^/]+)\\Z")
    elif path == reverse('admin:login'):
        return redirect('admin:login')
    else:
        return redirect('welcome')