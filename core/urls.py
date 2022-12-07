from django.urls import path

from core.views import evaluations, evaluation_view_form, user_statistics

urlpatterns = [
    path('<int:user_id>/evaluations/', evaluations, name='evaluations'),
    path('evaluate/<int:pk>/', evaluation_view_form, name='evaluation_form'),
    path('users/students/statistics/', user_statistics, name='user_statistics'),
]