from django.urls import path

from email_service.views import email_students, email_service, email_lecturers

urlpatterns = [
    path('', email_service, name='email_service'),
    path('students', email_students, name='email_students'),
    path('lectuers/', email_lecturers, name='email_lecturers'),
]