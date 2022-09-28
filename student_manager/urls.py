from django.urls import path

from student_manager.views import manager_students_view, students_managers

urlpatterns = [
    path('', manager_students_view, name='students_manager'),
    path('student-managers/', students_managers, name='students_managers'),
]