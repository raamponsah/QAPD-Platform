from django.core.paginator import Paginator
from django.db.models import Avg, F, Count
from django.shortcuts import render

# Create your views here.
from accounts.auth_decorators import only_lecturer, only_admins_and_lecturers, only_admins
from accounts.models import LecturerProfile, CustomUser
from compute.compute_constants import NUMBER_OF_ATTENDANCE_CHOICES, NUMBER_OF_DELIVERY_CHOICES, \
    NUMBER_OF_CUMULATIVE_CHOICES, NUMBER_OF_INTERACTION_CHOICES, NUMBER_OF_ASSIGNMENTS_CHOICES
from core.models import CourseInformation, Evaluation, EvaluationSubmission
from helper_functions.helpers import computational_stats, statistics

@only_lecturer
def lecturer_dashboard(request):
    if request.user.is_authenticated is False:
        return redirect('welcome')
    lecturer_user = CustomUser.objects.filter(id=request.user.id).get()
    lecturer_profile = LecturerProfile.objects.get(user=lecturer_user)
    lecturer_courses = CourseInformation.objects.filter(lecturer_code=lecturer_profile.staff_id)
    number_lecturer_courses = CourseInformation.objects.filter(lecturer_code=lecturer_profile.staff_id).count()

    evaluations = Evaluation.objects.filter(course__in=lecturer_courses, archived=False).select_related('course')
    number_of_evaluated_submissions = EvaluationSubmission.objects.filter(evaluationInfo__in=evaluations,
                                                                          is_evaluated=True).count()
    _reports = Evaluation.objects.all().annotate(submitted=Count(F('evaluation_form')))
    evaluation_submitted = Evaluation.objects.filter(course__in=lecturer_courses).annotate(
        submitted=Count(F('evaluation_form')))
    # Statistical Averaging
    cumulative_avg_stats = EvaluationSubmission.objects.filter(evaluationInfo__in=evaluation_submitted) \
        .annotate(cumulative_avg_submission=(Avg(F('curriculum_feedback_beginning_answer')) +
                                             Avg(F('curriculum_feedback_course_answer')) +
                                             Avg(F('curriculum_feedback_lecture_answer')) +
                                             Avg(F('curriculum_feedback_outcomes_answer')) +
                                             Avg(F('curriculum_feedback_procedures_answer')) +
                                             Avg(F('curriculum_feedback_books_answer'))
                                             )) \
        .aggregate((Avg('cumulative_avg_submission')))

    attendance_avg_stats = EvaluationSubmission.objects.filter(evaluationInfo__in=evaluation_submitted) \
        .annotate(attendance_avg_submission=(Avg(F('attendance_schedule')) +
                                             Avg(F('attendance_punctuality')) +
                                             Avg(F('attendance_presence'))
                                             )) \
        .aggregate((Avg('attendance_avg_submission')))

    delivery_avg_stats = EvaluationSubmission.objects.filter(evaluationInfo__in=evaluation_submitted) \
        .annotate(delivery_avg_submission=(Avg(F('delivery_enthusiasm')) +
                                           Avg(F('delivery_sequence')) +
                                           Avg(F('delivery_organization')) +
                                           Avg(F('delivery_clarity')) +
                                           Avg(F('delivery_contents')) +
                                           Avg(F('delivery_responsiveness')) +
                                           Avg(F('delivery_achievements')) +
                                           Avg(F('delivery_innovation')) +
                                           Avg(F('delivery_theory_practices'))
                                           )) \
        .aggregate((Avg('delivery_avg_submission')))

    assignments_avg_stats = EvaluationSubmission.objects.filter(evaluationInfo__in=evaluation_submitted) \
        .annotate(assignments_avg_submission=(Avg(F('assignments_relevance')) +
                                              Avg(F('assignments_promptitude')) +
                                              Avg(F('assignments_feedback')) +
                                              Avg(F('assignments_guidance'))

                                              )) \
        .aggregate((Avg('assignments_avg_submission')))

    interaction_avg_stats = EvaluationSubmission.objects.filter(evaluationInfo__in=evaluation_submitted) \
        .annotate(interaction_avg_submission=(Avg(F('interaction_availability')) +
                                              Avg(F('interaction_help')) +
                                              Avg(F('interaction_fairness'))
                                              )) \
        .aggregate((Avg('interaction_avg_submission')))

    averaged_cum_stats = round(
        float((cumulative_avg_stats['cumulative_avg_submission__avg']) / NUMBER_OF_CUMULATIVE_CHOICES), 2) if (
                                                                                                                  cumulative_avg_stats[
                                                                                                                      'cumulative_avg_submission__avg']) is not None else 0
    averaged_attendance_stats = round(
        float(attendance_avg_stats['attendance_avg_submission__avg']) / NUMBER_OF_ATTENDANCE_CHOICES, 2) if (
                                                                                                                attendance_avg_stats[
                                                                                                                    'attendance_avg_submission__avg']) is not None else 0
    averaged_delivery_stats = round(
        float(delivery_avg_stats['delivery_avg_submission__avg']) / NUMBER_OF_DELIVERY_CHOICES, 2) if (
                                                                                                          delivery_avg_stats[
                                                                                                              'delivery_avg_submission__avg']) is not None else 0
    averaged_assignments_stats = round(
        float(assignments_avg_stats['assignments_avg_submission__avg']) / NUMBER_OF_ASSIGNMENTS_CHOICES, 2) if (
                                                                                                                   assignments_avg_stats[
                                                                                                                       'assignments_avg_submission__avg']) is not None else 0

    averaged_interaction_stats = round(
        float(interaction_avg_stats['interaction_avg_submission__avg']) / NUMBER_OF_INTERACTION_CHOICES, 2) if (
                                                                                                                   interaction_avg_stats[
                                                                                                                       'interaction_avg_submission__avg']) is not None else 0

    total_score_cumulatively = round((
                                             averaged_cum_stats + averaged_attendance_stats + averaged_delivery_stats + averaged_assignments_stats + averaged_interaction_stats) / 5,
                                     2)

    grade = 'D'
    if float(total_score_cumulatively) > 3.5:
        grade = 'A'
    elif 3.0 < float(total_score_cumulatively) < 3.5:
        grade = 'B'
    elif 3.0 > float(total_score_cumulatively) > 2.5:
        grade = 'C'
    elif float(total_score_cumulatively) < 2.5:
        grade = 'D'

    context = {
            'total_score_cumulatively': total_score_cumulatively,
            'grade': grade,
            'active': 'levm',
            'page_obj': evaluations,
            'number_of_courses': number_lecturer_courses,
            'number_of_submissions': number_of_evaluated_submissions,
        }
    return render(request, 'lecturer_portal/dashboard.html', context)

@only_admins
def lecturers(request):
    all_lecturers = LecturerProfile.objects.all()
    paginator = Paginator(all_lecturers, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        **statistics(),
        'active':'levm'
    }
    return render(request, 'compute/admin-dashboard-lecturers.html', context)


@only_admins_and_lecturers
def lecturer_archived_reports(request):
    lecturer_user = CustomUser.objects.filter(id=request.user.id).first()
    lecturer_profile = LecturerProfile.objects.get(user=lecturer_user)
    lecturer_courses = CourseInformation.objects.filter(lecturer_code=lecturer_profile.staff_id)
    archived_evaluations_submitted = Evaluation.objects.filter(archived=True, course__in=lecturer_courses)
    number_lecturer_courses = CourseInformation.objects.filter(lecturer_code=lecturer_profile.staff_id).count()
    # find total number of students who take the specific course
    evaluations = Evaluation.objects.filter(course__in=lecturer_courses, archived=False).select_related('course')
    number_of_evaluated_submissions = EvaluationSubmission.objects.filter(evaluationInfo__in=evaluations,
                                                                          is_evaluated=True).count()
    # number_of_students_taught = Student.objects.filter(campus=lecturer_courses, program=program).count()
    _reports = Evaluation.objects.all().annotate(submitted=Count(F('evaluation_form')))

    # l_courses = CourseInformation.objects.filter(lecturer_code=lecturer_profile.staff_id)

    evaluation_submitted = Evaluation.objects.filter(course__in=lecturer_courses).annotate(
        submitted=Count(F('evaluation_form')))
    # Statistical Averaging
    cumulative_avg_stats = EvaluationSubmission.objects.filter(evaluationInfo__in=evaluation_submitted) \
        .annotate(cumulative_avg_submission=(Avg(F('curriculum_feedback_beginning_answer')) +
                                             Avg(F('curriculum_feedback_course_answer')) +
                                             Avg(F('curriculum_feedback_lecture_answer')) +
                                             Avg(F('curriculum_feedback_outcomes_answer')) +
                                             Avg(F('curriculum_feedback_procedures_answer')) +
                                             Avg(F('curriculum_feedback_books_answer'))
                                             )) \
        .aggregate((Avg('cumulative_avg_submission')))

    attendance_avg_stats = EvaluationSubmission.objects.filter(evaluationInfo__in=evaluation_submitted) \
        .annotate(attendance_avg_submission=(Avg(F('attendance_schedule')) +
                                             Avg(F('attendance_punctuality')) +
                                             Avg(F('attendance_presence'))
                                             )) \
        .aggregate((Avg('attendance_avg_submission')))

    delivery_avg_stats = EvaluationSubmission.objects.filter(evaluationInfo__in=evaluation_submitted) \
        .annotate(delivery_avg_submission=(Avg(F('delivery_enthusiasm')) +
                                           Avg(F('delivery_sequence')) +
                                           Avg(F('delivery_organization')) +
                                           Avg(F('delivery_clarity')) +
                                           Avg(F('delivery_contents')) +
                                           Avg(F('delivery_responsiveness')) +
                                           Avg(F('delivery_achievements')) +
                                           Avg(F('delivery_innovation')) +
                                           Avg(F('delivery_theory_practices'))
                                           )) \
        .aggregate((Avg('delivery_avg_submission')))

    assignments_avg_stats = EvaluationSubmission.objects.filter(evaluationInfo__in=evaluation_submitted) \
        .annotate(assignments_avg_submission=(Avg(F('assignments_relevance')) +
                                              Avg(F('assignments_promptitude')) +
                                              Avg(F('assignments_feedback')) +
                                              Avg(F('assignments_guidance'))

                                              )) \
        .aggregate((Avg('assignments_avg_submission')))

    interaction_avg_stats = EvaluationSubmission.objects.filter(evaluationInfo__in=evaluation_submitted) \
        .annotate(interaction_avg_submission=(Avg(F('interaction_availability')) +
                                              Avg(F('interaction_help')) +
                                              Avg(F('interaction_fairness'))
                                              )) \
        .aggregate((Avg('interaction_avg_submission')))

    averaged_cum_stats = round(
        float((cumulative_avg_stats['cumulative_avg_submission__avg']) / NUMBER_OF_CUMULATIVE_CHOICES), 2) if (
                                                                                                                  cumulative_avg_stats[
                                                                                                                      'cumulative_avg_submission__avg']) is not None else 0
    averaged_attendance_stats = round(
        float(attendance_avg_stats['attendance_avg_submission__avg']) / NUMBER_OF_ATTENDANCE_CHOICES, 2) if (
                                                                                                                attendance_avg_stats[
                                                                                                                    'attendance_avg_submission__avg']) is not None else 0
    averaged_delivery_stats = round(
        float(delivery_avg_stats['delivery_avg_submission__avg']) / NUMBER_OF_DELIVERY_CHOICES, 2) if (
                                                                                                          delivery_avg_stats[
                                                                                                              'delivery_avg_submission__avg']) is not None else 0
    averaged_assignments_stats = round(
        float(assignments_avg_stats['assignments_avg_submission__avg']) / NUMBER_OF_ASSIGNMENTS_CHOICES, 2) if (
                                                                                                                   assignments_avg_stats[
                                                                                                                       'assignments_avg_submission__avg']) is not None else 0

    averaged_interaction_stats = round(
        float(interaction_avg_stats['interaction_avg_submission__avg']) / NUMBER_OF_INTERACTION_CHOICES, 2) if (
                                                                                                                   interaction_avg_stats[
                                                                                                                       'interaction_avg_submission__avg']) is not None else 0

    total_score_cumulatively = round((
                                             averaged_cum_stats + averaged_attendance_stats + averaged_delivery_stats + averaged_assignments_stats + averaged_interaction_stats) / 5,
                                     2)

    # grade = 'D'
    # if float(total_score_cumulatively) > 3.5:
    #     grade = 'A'
    # elif 3.0 < float(total_score_cumulatively) < 3.5:
    #     grade = 'B'
    # elif 3.0 > float(total_score_cumulatively) > 2.5:
    #     grade = 'C'
    # elif float(total_score_cumulatively) < 2.5:
    #     grade = 'D'

    context = {
        'total_score_cumulatively': total_score_cumulatively,
        'page_obj': evaluations,
        'active': 'levm',
        'number_of_courses': number_lecturer_courses,
        'number_of_submissions': number_of_evaluated_submissions,
        'archived_evaluations_submitted': archived_evaluations_submitted,
    }

    return render(request, 'lecturer_portal/dashboard-archives.html', context)


@only_admins_and_lecturers
def lecturer(request, pk):
    lecturer_profile = LecturerProfile.objects.get(id=pk)
    lecturer_courses = CourseInformation.objects.filter(lecturer_code=lecturer_profile.staff_id)
    number_lecturer_courses = CourseInformation.objects.filter(lecturer_code=lecturer_profile.staff_id).count()
    # find total number of students who take the specific course
    evaluations = Evaluation.objects.filter(course__in=lecturer_courses, archived=False).select_related('course')
    number_of_evaluated_submissions = EvaluationSubmission.objects.filter(evaluationInfo__in=evaluations,
                                                                          is_evaluated=True).count()
    # number_of_students_taught = Student.objects.filter(campus=lecturer_courses, program=program).count()
    _reports = Evaluation.objects.all().annotate(submitted=Count(F('evaluation_form')))

    context = {
        'active': 'levm',
        'page_obj': evaluations,
        'number_of_courses': number_lecturer_courses,
        'number_of_submissions': number_of_evaluated_submissions,
        'lecturer_courses':lecturer_courses,
        'lecturer_profile':lecturer_profile
    }

    return render(request, 'lecturer_portal/dashboard.html', context)