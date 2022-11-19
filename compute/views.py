from django.core.paginator import Paginator
from django.db.models import Count, F, Avg, Sum, Max, Min, StdDev, Variance
from django.shortcuts import render, get_object_or_404

from accounts.auth_decorators import only_admins, only_lecturer, only_admins_and_lecturers
from accounts.models import LecturerProfile
from core.models import Evaluation, EvaluationSubmission, CourseInformation
from evaluation_manager.models import EvaluationManager
from helper_functions.helpers import statistics

NUMBER_OF_CUMULATIVE_CHOICES = 6
NUMBER_OF_ATTENDANCE_CHOICES = 3
NUMBER_OF_DELIVERY_CHOICES = 9
NUMBER_OF_ASSIGNMENTS_CHOICES = 9
NUMBER_OF_INTERACTION_CHOICES = 3
NUMBER_OF_ENVIRONMENT_CHOICES = 9


@only_admins_and_lecturers
def dashboard(request):
    _reports = Evaluation.objects.all().annotate(submitted=Count(F('evaluation_form')))
    e_submitted = EvaluationSubmission.objects.all()
    paginator = Paginator(e_submitted, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    evaluation_managers_list = EvaluationManager.objects.all().order_by('-end_date')
    courses = CourseInformation.objects.all()
    paginator_2 = Paginator(courses, 10)
    page_number_2 = request.GET.get('page')
    page_obj_2 = paginator_2.get_page(page_number_2)

    stats = statistics()
    context = {
        'active': 'compute',
        'evaluation_reports': _reports,
        'page_title': 'Evaluation Reports',
        'page_obj': page_obj,
        'evaluation_managers_list': evaluation_managers_list,
        'courses': page_obj_2,
        **stats
    }
    return render(request, 'compute/admin-dashboard.html', context)


# change the request parameter to lecturer id
@only_admins
def analytic_dashboard(request):
    stats = statistics()
    context = {
        'page_title': 'EV Analytic Dashboard',
        'active': 'compute',
        **stats
    }
    return render(request, 'compute/analysis/analytic_dashboard.html', context)


@only_admins_and_lecturers
def evaluation_reports_generated_list(request):
    stats = statistics()
    _reports = Evaluation.objects.filter(archived=True).annotate(submitted=Count(F('evaluation_form')))
    paginator = Paginator(_reports, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'active': 'evm',
        'evaluation_reports': _reports,
        'page_title': 'Evaluation Reports',
        'page_obj': page_obj,
        **stats
    }
    return render(request, 'compute/admin-dashboard.html', context)


@only_lecturer
def evaluation_reports_generated_list_archived(request):
    stats = statistics()
    _reports = Evaluation.objects.all().annotate(submitted=Count(F('evaluation_form')))
    paginator = Paginator(_reports, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'evaluation_reports': _reports,
        'page_title': 'Evaluation Reports',
        'page_obj': page_obj,
        'active': 'levm',
                  ** stats
    }
    return render(request, 'compute/admin-dashboard.html', context)


@only_admins_and_lecturers
def evaluation_report(request, slug):
    evaluation = get_object_or_404(Evaluation, slug=slug)
    lecturer = None
    if LecturerProfile.objects.filter(staff_id=evaluation.course.lecturer_code).get().count()==0:
        lecturer = LecturerProfile.objects.filter(staff_id=evaluation.course.lecturer_code).get()
    else:
        lecturer=None


    evaluation_submitted = Evaluation.objects.filter(slug=slug).annotate(
        submitted=Count(F('evaluation_form'))).get()

    e_curriculum_feedback_beginning_answer_stats = EvaluationSubmission.objects.filter(
        evaluationInfo=evaluation_submitted). \
        aggregate(Count(F('curriculum_feedback_beginning_answer')), Sum('curriculum_feedback_beginning_answer'),
                  Avg('curriculum_feedback_beginning_answer'),
                  Max(F('curriculum_feedback_beginning_answer')), Min(F('curriculum_feedback_beginning_answer')),
                  StdDev(F('curriculum_feedback_beginning_answer')),
                  Variance(F('curriculum_feedback_beginning_answer')),
                  )

    e_curriculum_feedback_course_answer_stats = EvaluationSubmission.objects.filter(
        evaluationInfo=evaluation_submitted). \
        aggregate(Count(F('curriculum_feedback_course_answer')), Sum('curriculum_feedback_course_answer'),
                  Avg('curriculum_feedback_course_answer'),
                  Max(F('curriculum_feedback_course_answer')), Min(F('curriculum_feedback_course_answer')),
                  StdDev(F('curriculum_feedback_course_answer')),
                  Variance(F('curriculum_feedback_course_answer')),
                  )

    e_curriculum_feedback_lecture_answer_stats = EvaluationSubmission.objects.filter(
        evaluationInfo=evaluation_submitted). \
        aggregate(Count(F('curriculum_feedback_lecture_answer')), Sum('curriculum_feedback_lecture_answer'),
                  Avg('curriculum_feedback_lecture_answer'),
                  Max(F('curriculum_feedback_lecture_answer')), Min(F('curriculum_feedback_lecture_answer')),
                  StdDev(F('curriculum_feedback_lecture_answer')),
                  Variance(F('curriculum_feedback_lecture_answer')),
                  )
    e_curriculum_feedback_outcomes_answer_stats = EvaluationSubmission.objects.filter(
        evaluationInfo=evaluation_submitted). \
        aggregate(Count(F('curriculum_feedback_outcomes_answer')), Sum('curriculum_feedback_outcomes_answer'),
                  Avg('curriculum_feedback_outcomes_answer'),
                  Max(F('curriculum_feedback_outcomes_answer')), Min(F('curriculum_feedback_outcomes_answer')),
                  StdDev(F('curriculum_feedback_outcomes_answer')),
                  Variance(F('curriculum_feedback_outcomes_answer')),
                  )

    e_curriculum_feedback_procedures_answer_stats = EvaluationSubmission.objects.filter(
        evaluationInfo=evaluation_submitted). \
        aggregate(Count(F('curriculum_feedback_procedures_answer')), Sum('curriculum_feedback_procedures_answer'),
                  Avg('curriculum_feedback_procedures_answer'),
                  Max(F('curriculum_feedback_procedures_answer')), Min(F('curriculum_feedback_procedures_answer')),
                  StdDev(F('curriculum_feedback_procedures_answer')),
                  Variance(F('curriculum_feedback_procedures_answer')),
                  )

    e_curriculum_feedback_books_answer_stats = EvaluationSubmission.objects.filter(
        evaluationInfo=evaluation_submitted). \
        aggregate(Count(F('curriculum_feedback_books_answer')), Sum('curriculum_feedback_books_answer'),
                  Avg('curriculum_feedback_books_answer'),
                  Max(F('curriculum_feedback_books_answer')), Min(F('curriculum_feedback_books_answer')),
                  StdDev(F('curriculum_feedback_books_answer')),
                  Variance(F('curriculum_feedback_books_answer')),
                  )

    # Attendance
    attendance_schedule = EvaluationSubmission.objects.filter(
        evaluationInfo=evaluation_submitted). \
        aggregate(Count(F('attendance_schedule')), Sum('attendance_schedule'),
                  Avg('attendance_schedule'),
                  Max(F('attendance_schedule')), Min(F('attendance_schedule')),
                  StdDev(F('attendance_schedule')),
                  Variance(F('attendance_schedule')),
                  )

    attendance_punctuality = EvaluationSubmission.objects.filter(
        evaluationInfo=evaluation_submitted). \
        aggregate(Count(F('attendance_punctuality')), Sum('attendance_punctuality'),
                  Avg('attendance_punctuality'),
                  Max(F('attendance_punctuality')), Min(F('attendance_punctuality')),
                  StdDev(F('attendance_punctuality')),
                  Variance(F('attendance_punctuality')),
                  )

    attendance_presence = EvaluationSubmission.objects.filter(
        evaluationInfo=evaluation_submitted). \
        aggregate(Count(F('attendance_presence')), Sum('attendance_presence'),
                  Avg('attendance_presence'),
                  Max(F('attendance_presence')), Min(F('attendance_presence')),
                  StdDev(F('attendance_presence')),
                  Variance(F('attendance_presence')),
                  )

    # Delivery
    delivery_enthusiasm = EvaluationSubmission.objects.filter(
        evaluationInfo=evaluation_submitted). \
        aggregate(Count(F('delivery_enthusiasm')), Sum('delivery_enthusiasm'),
                  Avg('delivery_enthusiasm'),
                  Max(F('delivery_enthusiasm')), Min(F('delivery_enthusiasm')),
                  StdDev(F('delivery_enthusiasm')),
                  Variance(F('delivery_enthusiasm')),
                  )

    delivery_sequence = EvaluationSubmission.objects.filter(
        evaluationInfo=evaluation_submitted). \
        aggregate(Count(F('delivery_sequence')), Sum('delivery_sequence'),
                  Avg('delivery_sequence'),
                  Max(F('delivery_sequence')), Min(F('delivery_sequence')),
                  StdDev(F('delivery_sequence')),
                  Variance(F('delivery_sequence')),
                  )

    delivery_organization = EvaluationSubmission.objects.filter(
        evaluationInfo=evaluation_submitted). \
        aggregate(Count(F('delivery_organization')), Sum('delivery_organization'),
                  Avg('delivery_organization'),
                  Max(F('delivery_organization')), Min(F('delivery_organization')),
                  StdDev(F('delivery_organization')),
                  Variance(F('delivery_organization')),
                  )

    delivery_clarity = EvaluationSubmission.objects.filter(
        evaluationInfo=evaluation_submitted). \
        aggregate(Count(F('delivery_clarity')), Sum('delivery_clarity'),
                  Avg('delivery_clarity'),
                  Max(F('delivery_clarity')), Min(F('delivery_clarity')),
                  StdDev(F('delivery_clarity')),
                  Variance(F('delivery_clarity')),
                  )

    delivery_contents = EvaluationSubmission.objects.filter(
        evaluationInfo=evaluation_submitted). \
        aggregate(Count(F('delivery_contents')), Sum('delivery_contents'),
                  Avg('delivery_contents'),
                  Max(F('delivery_contents')), Min(F('delivery_contents')),
                  StdDev(F('delivery_contents')),
                  Variance(F('delivery_contents')),
                  )

    delivery_responsiveness = EvaluationSubmission.objects.filter(
        evaluationInfo=evaluation_submitted). \
        aggregate(Count(F('delivery_responsiveness')), Sum('delivery_responsiveness'),
                  Avg('delivery_responsiveness'),
                  Max(F('delivery_responsiveness')), Min(F('delivery_responsiveness')),
                  StdDev(F('delivery_responsiveness')),
                  Variance(F('delivery_responsiveness')),
                  )

    delivery_achievements = EvaluationSubmission.objects.filter(
        evaluationInfo=evaluation_submitted). \
        aggregate(Count(F('delivery_achievements')), Sum('delivery_achievements'),
                  Avg('delivery_achievements'),
                  Max(F('delivery_achievements')), Min(F('delivery_achievements')),
                  StdDev(F('delivery_achievements')),
                  Variance(F('delivery_achievements')),
                  )

    delivery_innovation = EvaluationSubmission.objects.filter(
        evaluationInfo=evaluation_submitted). \
        aggregate(Count(F('delivery_innovation')), Sum('delivery_innovation'),
                  Avg('delivery_innovation'),
                  Max(F('delivery_innovation')), Min(F('delivery_innovation')),
                  StdDev(F('delivery_innovation')),
                  Variance(F('delivery_innovation')),
                  )

    delivery_theory_practices = EvaluationSubmission.objects.filter(
        evaluationInfo=evaluation_submitted). \
        aggregate(Count(F('delivery_theory_practices')), Sum('delivery_theory_practices'),
                  Avg('delivery_theory_practices'),
                  Max(F('delivery_theory_practices')), Min(F('delivery_theory_practices')),
                  StdDev(F('delivery_theory_practices')),
                  Variance(F('delivery_theory_practices')),
                  )

    assignments_relevance = EvaluationSubmission.objects.filter(
        evaluationInfo=evaluation_submitted). \
        aggregate(Count(F('assignments_relevance')), Sum('assignments_relevance'),
                  Avg('assignments_relevance'),
                  Max(F('assignments_relevance')), Min(F('assignments_relevance')),
                  StdDev(F('assignments_relevance')),
                  Variance(F('assignments_relevance')),
                  )

    assignments_promptitude = EvaluationSubmission.objects.filter(
        evaluationInfo=evaluation_submitted). \
        aggregate(Count(F('assignments_promptitude')), Sum('assignments_promptitude'),
                  Avg('assignments_promptitude'),
                  Max(F('assignments_promptitude')), Min(F('assignments_promptitude')),
                  StdDev(F('assignments_promptitude')),
                  Variance(F('assignments_promptitude')),
                  )
    assignments_feedback = EvaluationSubmission.objects.filter(
        evaluationInfo=evaluation_submitted). \
        aggregate(Count(F('assignments_feedback')), Sum('assignments_feedback'),
                  Avg('assignments_feedback'),
                  Max(F('assignments_feedback')), Min(F('assignments_feedback')),
                  StdDev(F('assignments_feedback')),
                  Variance(F('assignments_feedback')),
                  )

    assignments_guidance = EvaluationSubmission.objects.filter(
        evaluationInfo=evaluation_submitted). \
        aggregate(Count(F('assignments_guidance')), Sum('assignments_guidance'),
                  Avg('assignments_guidance'),
                  Max(F('assignments_guidance')), Min(F('assignments_guidance')),
                  StdDev(F('assignments_guidance')),
                  Variance(F('assignments_guidance')),
                  )

    interaction_availability = EvaluationSubmission.objects.filter(
        evaluationInfo=evaluation_submitted). \
        aggregate(Count(F('interaction_availability')), Sum('interaction_availability'),
                  Avg('interaction_availability'),
                  Max(F('interaction_availability')), Min(F('interaction_availability')),
                  StdDev(F('interaction_availability')),
                  Variance(F('interaction_availability')),
                  )

    interaction_help = EvaluationSubmission.objects.filter(
        evaluationInfo=evaluation_submitted). \
        aggregate(Count(F('interaction_help')), Sum('interaction_help'),
                  Avg('interaction_help'),
                  Max(F('interaction_help')), Min(F('interaction_help')),
                  StdDev(F('interaction_help')),
                  Variance(F('interaction_help')),
                  )

    interaction_fairness = EvaluationSubmission.objects.filter(
        evaluationInfo=evaluation_submitted). \
        aggregate(Count(F('interaction_fairness')), Sum('interaction_fairness'),
                  Avg('interaction_fairness'),
                  Max(F('interaction_fairness')), Min(F('interaction_fairness')),
                  StdDev(F('interaction_fairness')),
                  Variance(F('interaction_fairness')),
                  )

    environment_classroom_size = EvaluationSubmission.objects.filter(
        evaluationInfo=evaluation_submitted). \
        aggregate(Count(F('environment_classroom_size')), Sum('environment_classroom_size'),
                  Avg('environment_classroom_size'),
                  Max(F('environment_classroom_size')), Min(F('environment_classroom_size')),
                  StdDev(F('environment_classroom_size')),
                  Variance(F('environment_classroom_size')),
                  )

    environment_seats = EvaluationSubmission.objects.filter(
        evaluationInfo=evaluation_submitted). \
        aggregate(Count(F('environment_seats')), Sum('environment_seats'),
                  Avg('environment_seats'),
                  Max(F('environment_seats')), Min(F('environment_seats')),
                  StdDev(F('environment_seats')),
                  Variance(F('environment_seats')),
                  )

    environment_audio_visual_equip = EvaluationSubmission.objects.filter(
        evaluationInfo=evaluation_submitted). \
        aggregate(Count(F('environment_audio_visual_equip')), Sum('environment_audio_visual_equip'),
                  Avg('environment_audio_visual_equip'),
                  Max(F('environment_audio_visual_equip')), Min(F('environment_audio_visual_equip')),
                  StdDev(F('environment_audio_visual_equip')),
                  Variance(F('environment_audio_visual_equip')),
                  )

    environment_public_address = EvaluationSubmission.objects.filter(
        evaluationInfo=evaluation_submitted). \
        aggregate(Count(F('environment_public_address')), Sum('environment_public_address'),
                  Avg('environment_public_address'),
                  Max(F('environment_public_address')), Min(F('environment_public_address')),
                  StdDev(F('environment_public_address')),
                  Variance(F('environment_public_address')),
                  )

    environment_books = EvaluationSubmission.objects.filter(
        evaluationInfo=evaluation_submitted). \
        aggregate(Count(F('environment_books')), Sum('environment_books'),
                  Avg('environment_books'),
                  Max(F('environment_books')), Min(F('environment_books')),
                  StdDev(F('environment_books')),
                  Variance(F('environment_books')),
                  )

    environment_computers = EvaluationSubmission.objects.filter(
        evaluationInfo=evaluation_submitted). \
        aggregate(Count(F('environment_computers')), Sum('environment_computers'),
                  Avg('environment_computers'),
                  Max(F('environment_computers')), Min(F('environment_computers')),
                  StdDev(F('environment_computers')),
                  Variance(F('environment_computers')),
                  )

    environment_internet = EvaluationSubmission.objects.filter(
        evaluationInfo=evaluation_submitted). \
        aggregate(Count(F('environment_internet')), Sum('environment_internet'),
                  Avg('environment_internet'),
                  Max(F('environment_internet')), Min(F('environment_internet')),
                  StdDev(F('environment_internet')),
                  Variance(F('environment_internet')),
                  )

    environment_air_conditioning = EvaluationSubmission.objects.filter(
        evaluationInfo=evaluation_submitted). \
        aggregate(Count(F('environment_air_conditioning')), Sum('environment_air_conditioning'),
                  Avg('environment_air_conditioning'),
                  Max(F('environment_air_conditioning')), Min(F('environment_air_conditioning')),
                  StdDev(F('environment_air_conditioning')),
                  Variance(F('environment_air_conditioning')),
                  )

    environment_secretariat = EvaluationSubmission.objects.filter(
        evaluationInfo=evaluation_submitted). \
        aggregate(Count(F('environment_secretariat')), Sum('environment_secretariat'),
                  Avg('environment_secretariat'),
                  Max(F('environment_secretariat')), Min(F('environment_secretariat')),
                  StdDev(F('environment_secretariat')),
                  Variance(F('environment_secretariat')),
                  )

    # print("cumulative_stats", cumulative_stats)
    # cumulative_sum_stats = EvaluationSubmission.objects.filter(evaluationInfo=evaluation_submitted) \
    #     .annotate(cumulative_sum_submission=(Sum(F('curriculum_feedback_beginning_answer')) +
    #                                          Sum(F('curriculum_feedback_course_answer')) +
    #                                          Sum(F('curriculum_feedback_lecture_answer')) +
    #                                          Sum(F('curriculum_feedback_outcomes_answer')) +
    #                                          Sum(F('curriculum_feedback_procedures_answer')) +
    #                                          Sum(F('curriculum_feedback_books_answer'))
    #                                          )) \
    #     .aggregate(Sum('cumulative_sum_submission'))

    # Statistical Averaging
    cumulative_avg_stats = EvaluationSubmission.objects.filter(evaluationInfo=evaluation_submitted) \
        .annotate(cumulative_avg_submission=(Avg(F('curriculum_feedback_beginning_answer')) +
                                             Avg(F('curriculum_feedback_course_answer')) +
                                             Avg(F('curriculum_feedback_lecture_answer')) +
                                             Avg(F('curriculum_feedback_outcomes_answer')) +
                                             Avg(F('curriculum_feedback_procedures_answer')) +
                                             Avg(F('curriculum_feedback_books_answer'))
                                             )) \
        .aggregate((Avg('cumulative_avg_submission')))

    attendance_avg_stats = EvaluationSubmission.objects.filter(evaluationInfo=evaluation_submitted) \
        .annotate(attendance_avg_submission=(Avg(F('attendance_schedule')) +
                                             Avg(F('attendance_punctuality')) +
                                             Avg(F('attendance_presence'))
                                             )) \
        .aggregate((Avg('attendance_avg_submission')))

    delivery_avg_stats = EvaluationSubmission.objects.filter(evaluationInfo=evaluation_submitted) \
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

    assignments_avg_stats = EvaluationSubmission.objects.filter(evaluationInfo=evaluation_submitted) \
        .annotate(assignments_avg_submission=(Avg(F('assignments_relevance')) +
                                              Avg(F('assignments_promptitude')) +
                                              Avg(F('assignments_feedback')) +
                                              Avg(F('assignments_guidance'))

                                              )) \
        .aggregate((Avg('assignments_avg_submission')))

    interaction_avg_stats = EvaluationSubmission.objects.filter(evaluationInfo=evaluation_submitted) \
        .annotate(interaction_avg_submission=(Avg(F('interaction_availability')) +
                                              Avg(F('interaction_help')) +
                                              Avg(F('interaction_fairness'))

                                              )) \
        .aggregate((Avg('interaction_avg_submission')))

    environment_avg_stats = EvaluationSubmission.objects.filter(evaluationInfo=evaluation_submitted) \
        .annotate(environment_avg_submission=(Avg(F('environment_classroom_size')) +
                                              Avg(F('environment_seats')) +
                                              Avg(F('environment_audio_visual_equip')) +
                                              Avg(F('environment_public_address')) +
                                              Avg(F('environment_books')) +
                                              Avg(F('environment_computers')) +
                                              Avg(F('environment_internet')) +
                                              Avg(F('environment_air_conditioning')) +
                                              Avg(F('environment_secretariat'))

                                              )) \
        .aggregate((Avg('environment_avg_submission')))

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
    averaged_environment_stats = round(
        float(environment_avg_stats['environment_avg_submission__avg']) / NUMBER_OF_ENVIRONMENT_CHOICES, 2) if (
                                                                                                                   environment_avg_stats[
                                                                                                                       'environment_avg_submission__avg']) is not None else 0
    total_score_cumulatively = round((
                                             averaged_cum_stats + averaged_attendance_stats + averaged_delivery_stats + averaged_assignments_stats + averaged_interaction_stats) / 5,
                                     2)
    context = {
        'evaluation': evaluation,
        'page_title': f"{evaluation_submitted} Report",
        'evaluation_submitted': evaluation_submitted,

        'averaged_cum_stats': averaged_cum_stats,
        'averaged_attendance_stats': averaged_attendance_stats,
        'averaged_delivery_stats': averaged_delivery_stats,
        'averaged_assignments_stats': averaged_assignments_stats,
        'averaged_interaction_stats': averaged_interaction_stats,
        'averaged_environment_stats': averaged_environment_stats,

        'total_score_cumulatively': total_score_cumulatively,

        'curriculum': {
            "beginning": e_curriculum_feedback_beginning_answer_stats,
            "course": e_curriculum_feedback_course_answer_stats,
            "lecture": e_curriculum_feedback_lecture_answer_stats,
            "outcomes": e_curriculum_feedback_outcomes_answer_stats,
            "procedures": e_curriculum_feedback_procedures_answer_stats,
            "books": e_curriculum_feedback_books_answer_stats,

        },

        'cumulative_avg_stats': cumulative_avg_stats,
        'attendance': {
            'schedule': attendance_schedule,
            'punctuality': attendance_punctuality,
            'presence': attendance_presence,
        },
        'delivery': {
            'enthusiasm': delivery_enthusiasm,
            'sequence': delivery_sequence,
            'organization': delivery_organization,
            'clarity': delivery_clarity,
            'contents': delivery_contents,
            'responsiveness': delivery_responsiveness,
            'achievements': delivery_achievements,
            'innovation': delivery_innovation,
            'theory practices': delivery_theory_practices
        },
        'assignments': {
            'relevance': assignments_relevance,
            'promptitude': assignments_promptitude,
            'feedback': assignments_feedback,
            'guidance': assignments_guidance
        },
        'interactions': {
            'availability': interaction_availability,
            'help': interaction_help,
            'fairness': interaction_fairness
        },

        'environment': {
            'classroom size': environment_classroom_size,
            'seats': environment_seats,
            'audio visual equip': environment_audio_visual_equip,
            'public address': environment_public_address,
            'books': environment_books,
            'computers': environment_computers,
            'internet': environment_internet,
            'environment air conditioning': environment_air_conditioning,
            'environment secretariat': environment_secretariat

        },
        'lecturer': lecturer,
        'active': 'evm',
    }

    return render(request, 'compute/single-report.html', context)