from django.db import IntegrityError
from import_export import resources
from core.models import CourseInformation, ProgramInformation, CampusInformation


class SchoolDataResource(resources.ModelResource):
    class Meta:
        model = CourseInformation
        fields = (
            'academic_year',
            'campus_name',
            'faculty_school_name',
            'department_name',
            'qualification_name',
            'lecturer_code',
            'subject_code',
            'subject_name',
            'semester',
            'level',
            'course_group'
        )
        skip_unchanged = True
        report_skipped = True

    def save_instance(self, instance, using_transactions=True, dry_run=False):
        try:
            super().save_instance(instance, using_transactions, dry_run)
        except IntegrityError:
            pass

    # def save_instance(self, instance, using_transactions=True, dry_run=False):
    #     try:
    #         super(SchoolDataResource, self).save_instance(instance, using_transactions, dry_run)
    #     except IntegrityError:
    #         pass


class ProgramInformationResource(resources.ModelResource):
    class Meta:
        model = ProgramInformation
        fields = ('id', 'program_name', 'department_name')


class CampusInformationResource(resources.ModelResource):
    class Meta:
        model = CampusInformation
        fields = ('id', 'campus_name',)