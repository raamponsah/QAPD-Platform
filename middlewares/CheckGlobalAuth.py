from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.urls import reverse


class CheckGlobalAuth:
    def __init__(self, get_response):
        self.get_response = get_response

        self.exception_urls = list([
            reverse('admin:login'),
            reverse('welcome'),
            reverse('login_student'),
            reverse('login_lecturer'),
            reverse('login_administrator'),
            reverse('register_student'),
            reverse('register_lecturer'),
        ])

    def __call__(self, request):
        response = self.get_response(request)
        if not request.user.is_authenticated:
            if request.path not in self.exception_urls:
                return self.utilityfunc(response)
        return response

    def utilityfunc(self, rpath):
        if rpath in self.exception_urls:
            return redirect(rpath)
        else:
            return redirect('welcome')