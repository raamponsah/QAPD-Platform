from django.urls import path

from core.views import evaluations, evaluation_view_form, user_statistics

urlpatterns = [
    path('<int:user_id>/evaluations/', evaluations, name='evaluations'),
    path('<int:user_id>/evaluations/<int:pk>/evaluate/', evaluation_view_form, name='evaluation_form'),
    path('users/students/statistics/', user_statistics, name='user_statistics'),
]