from django.urls import path

from core.views import evaluations, evaluation_view_form, student_user_statistics

urlpatterns = [
    path('', evaluations, name='evaluations'),
    path('evaluate/<int:pk>/', evaluation_view_form, name='evaluation_form'),
    path('users/students/statistics/', student_user_statistics, name='student_user_statistics'),
]