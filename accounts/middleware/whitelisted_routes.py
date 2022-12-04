from django.urls import reverse


def whitelisted_urls(request):
    return [
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
    ]