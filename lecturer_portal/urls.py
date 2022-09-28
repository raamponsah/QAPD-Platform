from django.urls import path


from lecturer_portal.views import lecturer_dashboard, lecturers, lecturer_archived_reports, lecturer

urlpatterns = [
    path('dashboard/', lecturer_dashboard, name='lecturer_dashboard'),
    # path('<int:lecturer_id>/profile/', lecturer_profile, name='lecturer-profile'),
    path('', lecturers, name='lecturers'),
    path('<int:pk>', lecturer, name='lecturer'),
    path('lecturer-archived-reports/', lecturer_archived_reports, name='lecturer_archived_reports'),

]