from django.contrib import admin

# Register your models here.
from import_export.admin import ImportExportModelAdmin

from core.models import CourseInformation, Evaluation, EvaluationSubmission, ProgramInformation, CampusInformation, \
    School

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


admin.site.register(CourseInformation, CourseAdminResource)


class ProgramInformationAdminResource(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('program_name',
                    'department_name','school')


admin.site.register(ProgramInformation, ProgramInformationAdminResource)


class CampusInformationAdminResource(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('campus_name',)


admin.site.register(CampusInformation, CampusInformationAdminResource)
admin.site.register(School)

from django.contrib import admin

# Register your models here.