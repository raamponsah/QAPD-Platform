from django.contrib import messages
from django.shortcuts import render, redirect

# Create your views here.
from accounts.auth_decorators import only_admins
from accounts.models import Student
from core.models import CampusInformation


@only_admins
def manager_students_view(request):
    students = Student.objects.all()
    if students:
        if request.method == 'POST':
            for student in students:
                Student.objects.filter(id=student.id).update(level=int(student.level) + 1)  # changed to 1
            messages.success(request, 'Students\' levels have been updated')
            return redirect('dashboard')
    else:
        return redirect('dashboard')
    # return render(request, 'student_manager/index.html', context)


def students_managers(request):
    campuses = CampusInformation.objects.all()
    return render(request, 'student_manager/index.html')