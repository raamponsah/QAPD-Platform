from django.shortcuts import redirect
from django.urls import reverse

from accounts.models import Student, CustomUser


def spm(get_response):
    def middleware(request):
        response = get_response(request)
        student = CustomUser.objects.get(id=request.user.id)
        print("from student router => ", student)
        try:
            if student is not None and student.is_student is True and student.is_active is True:
                return response
        except Student.DoesNotExist:
            while not (request.path == reverse('student_profile_create', kwargs={'pk': request.user.id})):
                return redirect(reverse('student_profile_create', kwargs={'pk': request.user.id}))
    return middleware