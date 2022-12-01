from django.contrib import messages
from django.shortcuts import render, redirect

# Create your views here.
from accounts.auth_decorators import only_student, only_admins
from accounts.models import Student, CustomUser, LecturerProfile
from core.forms import EvaluationForm
from core.models import Evaluation, EvaluationSubmission, CourseInformation


# SEMESTER_SWITCH = 1

# Auth Checks

@only_student
def evaluations(request):
    if request.user.is_authenticated is not True: # if user is not logged in
        return redirect('login_student')
    if request.user.is_student is False: # if user is a student
        return redirect('login_student')
    student = CustomUser.objects.filter(id=request.user.id).get()
    if student is None:
        return redirect('welcome')
    student_profile = Student.objects.filter(user=student).get()
    qualification_name = student_profile.program,
    # campus_name = student_profile.campus, level = student_profile.level
    school_data = CourseInformation.objects.filter(campus_name=student_profile.campus,
                                                   qualification_name=student_profile.program,
                                                   level=student_profile.level)
    lecturer_profiles = LecturerProfile.objects.all()
    evaluated_submissions = EvaluationSubmission.objects.filter(submitter=student_profile).values_list('evaluationInfo')
    evaluation_set = Evaluation.objects.filter(course__in=school_data, ended=False).exclude(
        id__in=evaluated_submissions).select_related('course')

    existing_courses = []
    for lecturer in lecturer_profiles:
        for evaluation in evaluation_set:
            if evaluation.course.lecturer_code == lecturer.staff_id:
                existing_courses.append(evaluation.course)

    context = {'evaluations': existing_courses, 'page_title': 'Evaluations', 'lecturers': lecturer_profiles}
    return render(request, 'core/evaluations.html', context)


@only_student
def evaluation_view_form(request, pk):
    student = Student.objects.filter(user=request.user.id).get()
    evaluation_instance = Evaluation.objects.filter(pk=pk).get()
    evaluation_form = EvaluationForm(initial={'evaluationInfo': evaluation_instance})

    if request.method == 'POST':
        evaluation_form = EvaluationForm(request.POST, initial={'evaluationInfo': evaluation_instance,
                                                                'submitter': request.user.id})
        if evaluation_form.is_valid():
            EvaluationSubmission(submitter=student, evaluationInfo=evaluation_instance,
                                 **evaluation_form.cleaned_data).save()
            messages.success(request, f"Thank you for evaluating!")
            return redirect('evaluations')
        else:
            print(evaluation_form.errors)
            messages.error(request, f"Some questions were not answered, please check.")
            evaluation_form = EvaluationForm(request.POST, initial={'evaluationInfo': evaluation_instance,
                                                                    'submitter': request.user.id})
    context = {'evaluation': evaluation_instance, 'evaluation_form': evaluation_form}
    return render(request, 'core/evaluation_form.html', context)


@only_admins
def user_statistics(request):
    students_with_profiles = Student.objects.all().count()
    all_student_users = CustomUser.objects.filter(is_student=True, is_active=True).count()
    all_non_active_students = CustomUser.objects.filter(is_student=True, is_active=False).count()
    students_who_have_evaluated = EvaluationSubmission.objects.all().distinct('submitter').count()

    lecturers_with_profiles = LecturerProfile.objects.all().count()
    all_lecturer_users = CustomUser.objects.filter(is_lecturer=True, is_active=True).count()
    all_non_active_lecturers = CustomUser.objects.filter(is_lecturer=True, is_active=False).count()

    context = {
        'students_with_profiles': students_with_profiles,
        'all_non_active_students': all_non_active_students,
        'all_student_users': all_student_users,
        'students_who_have_evaluated': students_who_have_evaluated,
        'page_title': 'Student Statistics',
        'lecturers_with_profiles': lecturers_with_profiles,
        'all_non_active_lecturers': all_non_active_lecturers,
        'all_lecturer_users': all_lecturer_users,

    }

    return render(request, 'core/user_statistics.html', context)