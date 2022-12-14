from django.contrib import messages
from django.shortcuts import render, redirect

# Create your views here.
from accounts.auth_decorators import only_student
from accounts.models import Student, CustomUser
from core.forms import EvaluationForm
from core.models import Evaluation, EvaluationSubmission, CourseInformation


# SEMESTER_SWITCH = 1


@only_student
def evaluations(request):
    student = CustomUser.objects.filter(id=request.user.id).get()
    student_profile = Student.objects.filter(user=student).get()
    qualification_name = student_profile.program,
    # campus_name = student_profile.campus, level = student_profile.level
    school_data = CourseInformation.objects.filter(campus_name=student_profile.campus,
                                                   qualification_name=student_profile.program, level=student_profile.level)
    evaluated_submissions = EvaluationSubmission.objects.filter(submitter=student_profile).values_list('evaluationInfo')
    evaluation_set = Evaluation.objects.filter(course__in=school_data, ended=False).exclude(id__in=evaluated_submissions)

    context = {'evaluations': evaluation_set, 'page_title': 'Evaluations'}
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
            evaluation_form = EvaluationForm(request.POST, initial={'evaluationInfo': evaluation_instance,
                                                                    'submitter': request.user.id})
    context = {'evaluation': evaluation_instance, 'evaluation_form': evaluation_form}
    return render(request, 'core/evaluation_form.html', context)