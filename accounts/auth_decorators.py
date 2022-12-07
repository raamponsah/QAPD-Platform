from django.http import HttpResponseBadRequest, HttpResponse
from django.shortcuts import redirect

from accounts.models import Student, CustomUser


def only_admins_and_lecturers(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_qadmin is True or request.user.is_lecturer:
            if request.user.is_qadmin or request.user.is_lecturer:
                return view_func(request, *args, **kwargs)
        else:
            return redirect('welcome')

    return wrapper_func


def only_admins(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_qadmin is True:
            if request.user.is_qadmin:
                return view_func(request, *args, **kwargs)
        else:
            return redirect('login_administrator')

    return wrapper_func


def only_student(view_func):
    def wrapper_func(request, *args, **kwargs):
        user = CustomUser.objects.filter(id=request.user.id).get()
        if request.user.is_authenticated and user.is_student is True and user.is_active is True:
            return view_func(request, *args, **kwargs)
        else:
            return redirect('login_student')
            # return HttpResponse('401 Unauthorized: You are not authorised to view this page.', status=401)
    return wrapper_func


def only_lecturer(view_func):
    def wrapper_func(request, *args, **kwargs):
        user = CustomUser.objects.filter(id=request.user.id).get()
        if request.user.is_authenticated and user.is_lecturer is True and user.is_active is True:
            return view_func(request, *args, **kwargs)
        else:
            return redirect('login_lecturer')
            # return HttpResponse('401 Unauthorized: You are not authorised to view this page.', status=401)
    return wrapper_func


def allowed_groups(permitted_groups=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
                if group in permitted_groups:
                    return view_func(request, *args, **kwargs)
                if group == 'qasa':
                    return redirect('analytic_dashboard')
                elif group == 'student':
                    return redirect('evaluations')
                else:
                    return HttpResponse('401 Unauthorized: You are not authorised to view this page.', status=401)
            else:
                return HttpResponse('401 Unauthorized: You are not authorised to view this page.', status=401)

        return wrapper_func

    return decorator