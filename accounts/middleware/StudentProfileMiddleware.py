from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse

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


# def check_authenticated_user(get_response):
#     def middleware(request):
#         response = get_response(request)
#         if request.user.id is None:
#             while request.path not in list([reverse('admin:login'), reverse('login'), reverse('register_user')]):
#                 return utilityfunc(request.path)
#         return response
#
#     return middleware


# def utilityfunc(path):
#     if path == reverse('login_student'):
#         return redirect('login_student')
#     elif path == reverse('register_user'):
#         return redirect('register_user')
#     elif path == reverse('admin:login'):
#         return redirect('admin:login')
#     elif path == reverse('welcome'):
#         return redirect('welcome')
#     elif path == reverse('redirect_to_welcome'):
#         return redirect('redirect_to_welcome')
#     else:
#         return redirect('welcome')