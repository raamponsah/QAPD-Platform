from django.urls import path

from reports.views import school_report_summary, school_reports_grouped_by_academic_year, select_schools_academic_year, \
    select_global_academic_year, global_reports_grouped_by_academic_year, select_facilities_academic_year, \
    facilities_reports_grouped_by_academic_year

urlpatterns = [
    path('select/global-academic-year/', select_global_academic_year, name='select_global_academic_year'),

    path('grouped-by/<int:evm_id>/global/', global_reports_grouped_by_academic_year,
         name='global_reports_grouped_by_academic_year'),
    path('select/schools-academic-year/', select_schools_academic_year, name='select_schools_academic_year'),
    path('grouped-by/<int:evm_id>/schools/', school_reports_grouped_by_academic_year,
         name='school_reports_grouped_by_academic_year'),
    path('grouped-by/schools/<int:school_id>/academic-year/<slug:slug>/', school_report_summary,
         name='school_report_summary'),

    path('select/facilities-academic-year/', select_facilities_academic_year, name='select_facilities_academic_year'),
    path('grouped-by/<int:evm_id>/global/facilities/', facilities_reports_grouped_by_academic_year,
         name='facilities_reports_grouped_by_academic_year'),

]