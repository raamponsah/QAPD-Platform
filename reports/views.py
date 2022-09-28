from django.db.models import Count
from django.shortcuts import render

# Create your views here.
from accounts.models import LecturerProfile
from core.models import CourseInformation, School, EvaluationSubmission, Evaluation
from evaluation_manager.models import EvaluationManager
from helper_functions.helpers import computational_global_stats, computational_school_stats


def select_schools_academic_year(request):
    evaluation_managers = EvaluationManager.objects.all().order_by('academic_year', 'semester')
    return render(request, 'reports/grouped_by_year.html', {'page_obj': evaluation_managers, 'active': 'school-report'})


def school_reports_grouped_by_academic_year(request, evm_id):
    evaluation_manager = EvaluationManager.objects.filter(id=evm_id).first()
    evaluation_managers = EvaluationManager.objects.all().order_by('academic_year', 'semester')
    academic_year_under_review = evaluation_manager.academic_year
    semester_under_review = evaluation_manager.semester
    schools = School.objects.all()
    courses = CourseInformation.objects.filter(academic_year=academic_year_under_review, semester=semester_under_review) \
        .annotate(n_courses=Count('subject_code'))
    evaluations = Evaluation.objects.filter(course__in=courses)
    e_submissions = EvaluationSubmission.objects.filter(evaluationInfo__in=evaluations)
    cgs = computational_global_stats(courses)

    return render(request, 'reports/index.html', {'page_obj': schools,
                                                  'evm': evaluation_manager,
                                                  'evms': evaluation_managers,
                                                  'academic_year': academic_year_under_review,
                                                  'semester': semester_under_review,
                                                  'active': 'school-report',
                                                  'cgs': cgs,
                                                  'n_courses': courses.count(),
                                                  'e_submissions': e_submissions.count()
                                                  })


def school_report_summary(request, school_id, slug):
    school = School.objects.get(id=school_id)
    evaluation_manager = EvaluationManager.objects.filter(slug=slug).first()
    ay = evaluation_manager.academic_year
    se = evaluation_manager.semester
    school_courses = CourseInformation.objects.filter(faculty_school_name=school.name, academic_year=ay, semester=se)
    school_courses_vl = CourseInformation.objects.filter(faculty_school_name=school.name, academic_year=ay, semester=se) \
        .values_list('lecturer_code', flat=True)
    evaluations = Evaluation.objects.filter(course__in=school_courses)
    e_submissions = EvaluationSubmission.objects.filter(evaluationInfo__in=evaluations)
    cgs = computational_school_stats(school_courses)
    lecturers = LecturerProfile.objects.all()
    context = {
        'school': school,
        'school_courses': school_courses,
        'lecturers': lecturers,
        'active': 'school-report',
        'school_courses_vl': school_courses_vl,
        'cgs': cgs,
        'n_courses': school_courses.count(),
        'e_submissions': e_submissions.count(),
        'academic_year': ay,
        'semester': se,
        'page_title': 'Evaluation'
    }

    return render(request, 'reports/school_stats.html', context)


# Global report functions
def select_global_academic_year(request):
    evaluation_managers = EvaluationManager.objects.all().order_by('academic_year', 'semester')
    e_submissions = EvaluationSubmission.objects.filter(is_evaluated=True).count()
    return render(request, 'reports/global_grouped_by_year.html',
                  {'page_obj': evaluation_managers, 'active': 'global-report',
                   'e_submissions': e_submissions,
                   })


def global_reports_grouped_by_academic_year(request, evm_id):
    evaluation_manager = EvaluationManager.objects.filter(id=evm_id).first()
    evaluation_managers = EvaluationManager.objects.all().order_by('academic_year', 'semester')
    academic_year_under_review = evaluation_manager.academic_year
    semester_under_review = evaluation_manager.semester
    schools = School.objects.all()
    e_submissions = EvaluationSubmission.objects.filter(is_evaluated=True).count()

    courses = CourseInformation.objects.filter(academic_year=academic_year_under_review,
                                               semester=semester_under_review)
    courses_vl = CourseInformation.objects.filter(academic_year=academic_year_under_review,
                                                  semester=semester_under_review) \
        .values_list('lecturer_code', flat=True)
    lecturers = LecturerProfile.objects.all()
    n_courses = CourseInformation.objects.all().count()

    cgs = computational_global_stats(courses)
    context = {'page_obj': schools,
               'evm': evaluation_manager,
               'evms': evaluation_managers,
               'academic_year': academic_year_under_review,
               'semester': semester_under_review,
               'active': 'global-report',
               'courses_vl': courses_vl,
               'courses': courses,
               'lecturers': lecturers,
               'e_submissions': e_submissions,
               'n_courses': n_courses,
               'cgs': cgs
               }
    return render(request, 'reports/global_stats.html', context)


# facilities Report
def select_facilities_academic_year(request):
    evaluation_managers = EvaluationManager.objects.all().order_by('academic_year', 'semester')
    return render(request, 'reports/facilities_grouped_by_year.html', {'page_obj': evaluation_managers,
                                                                       'active': 'facilities-report'})

def facilities_reports_grouped_by_academic_year(request, evm_id):
    evaluation_manager = EvaluationManager.objects.filter(id=evm_id).first()
    evaluation_managers = EvaluationManager.objects.all().order_by('academic_year', 'semester')
    academic_year_under_review = evaluation_manager.academic_year
    semester_under_review = evaluation_manager.semester
    schools = School.objects.all()
    e_submissions = EvaluationSubmission.objects.filter(is_evaluated=True).count()

    courses = CourseInformation.objects.filter(academic_year=academic_year_under_review,
                                               semester=semester_under_review)
    courses_vl = CourseInformation.objects.filter(academic_year=academic_year_under_review,
                                                  semester=semester_under_review) \
        .values_list('lecturer_code', flat=True)
    lecturers = LecturerProfile.objects.all()
    n_courses = CourseInformation.objects.all().count()

    cgs = computational_global_stats(courses)
    context = {'page_obj': schools,
               'evm': evaluation_manager,
               'evms': evaluation_managers,
               'academic_year': academic_year_under_review,
               'semester': semester_under_review,
               'active': 'global-report',
               'courses_vl': courses_vl,
               'courses': courses,
               'lecturers': lecturers,
               'e_submissions': e_submissions,
               'n_courses': n_courses,
               'cgs': cgs
               }
    return render(request, 'reports/global_stats.html', context)