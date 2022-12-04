from django.http import HttpRequest
from django.urls import reverse


def whitelisted_urls(request):
    return [
        reverse('admin:login'),
        reverse('welcome'),
        reverse('login_student'),
        reverse('login_lecturer'),
        reverse('login_administrator'),
        reverse('register_student'),
        reverse('register_lecturer'),

        reverse('password_reset_confirm',
                kwargs={'uidb64': request.path.split('/')[0] if request.path.split('/')[0] else None,
                        'token': request.path.split('/')[0] if request.path.split('/')[0] else None}),

        reverse('password_reset_request'),
        reverse('password_change'),
        reverse('password_reset_done'),
        reverse('password_reset_complete'),
    ]