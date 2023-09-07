from django.urls import path

from lecturer_portal.views import lecturer_dashboard
from .views import evaluation_reports_generated_list, evaluation_report, dashboard, \
    evaluation_reports_generated_list_archived

urlpatterns = [

    path('dashboard/', dashboard, name='dashboard'),
    path('reports/', evaluation_reports_generated_list, name='evaluation_reports_generated_list'),

    path('archived-reports/', evaluation_reports_generated_list_archived,
         name='evaluation_reports_generated_list_archived'),
    path('reports/<int:staff_id>/<str:subject_name>', evaluation_report, name='evaluation_report'),



]