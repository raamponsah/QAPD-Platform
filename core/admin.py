from django.contrib import admin

# Register your models here.
from import_export.admin import ImportExportModelAdmin

from core.models import CourseInformation, Evaluation, EvaluationSubmission, ProgramInformation, CampusInformation, \
    School
from core.resources import ProgramInformationResource, SchoolListResource, CampusInformationResource, SchoolDataResource

admin.site.register(Evaluation)
admin.site.register(EvaluationSubmission)


class CourseAdminResource(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('academic_year',
                    'campus_name',
                    'faculty_school_name',
                    'department_name',
                    'qualification_name',
                    'lecturer_code',
                    'subject_code',
                    'subject_name',
                    'semester',
                    'level',
                    'course_group',

                    )
    search_fields = ['subject_code', 'subject_name', 'qualification_name', 'campus_name', ]
    resource_class = SchoolDataResource


admin.site.register(CourseInformation, CourseAdminResource)


class ProgramInformationAdminResource(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('program_name',
                    'department_name', 'school')
    resource_class = ProgramInformationResource


admin.site.register(ProgramInformation, ProgramInformationAdminResource)


class CampusInformationAdminResource(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('campus_name',)
    resource_class = CampusInformationResource


admin.site.register(CampusInformation, CampusInformationAdminResource)


class SchoolAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('name',)
    resource_class = SchoolListResource


admin.site.register(School, SchoolAdmin)

from django.contrib import admin

# Register your models here.