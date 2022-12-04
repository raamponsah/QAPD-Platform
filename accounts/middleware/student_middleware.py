from django.shortcuts import redirect
from django.urls import reverse

from accounts.middleware.LecturerProfileMiddleware import utilityfunc
from accounts.models import Student


def router_middleware(get_response):
    def middleware(request):
        reset_pattern_url = '/accounts/reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$'
        exception_urls_ = [reverse('admin:login'),
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
                           ]

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
        reset_pattern_url = '/accounts/reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$'
        exception_urls_ = [reverse('admin:login'),
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
                           ]

        response = get_response(request)
        if request.user.id is None:
            while request.path not in list(exception_urls_):
                return utilityfunc(request.path)
        return response

    return middleware