from django.contrib import messages
from django.shortcuts import render

# Create your views here.
from accounts.email import send_bulk_mail
from accounts.models import CustomUser


def email_service(request):
    if request.method == 'POST':
        if request.POST['sendto'] == 'students':
            email_students(request.POST['subject'], request.POST['message'])
            messages.success(request, f"Emails sent!")
        elif request.POST['sendto'] == 'lecturers':
            email_lecturers(request.POST['subject'], request.POST['message'])
            messages.success(request, f"Emails sent!")

    return render(request, 'email_service/index.html',{'active':'es'})


def email_students(subject, message):
    students = CustomUser.objects.filter(is_student=True, is_active=True)
    bulk = []
    for student in students:
        bulk.append(
            {
                "Email": student.email,
                "Name": student.first_name
            }
        )

        return send_bulk_mail(bulk, subject, message)


def email_lecturers(subject, message):
    lecturers = CustomUser.objects.filter(is_lecturer=True, is_active=True)

    bulk = []
    for lecturer in lecturers:
        bulk.append(
            {
                "Email": lecturer.email,
                "Name": lecturer.first_name
            }
        )

        return send_bulk_mail(bulk, subject, message)