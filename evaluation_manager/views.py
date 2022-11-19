from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import render, redirect

# Create your views here.
from accounts.auth_decorators import only_admins
from accounts.email import send_bulk_mail
from accounts.models import CustomUser
from core.models import Evaluation
from evaluation_manager.forms import EvaluationManagerForm
from evaluation_manager.models import EvaluationManager
from helper_functions.helpers import statistics


@only_admins
def evaluation_managers_view(request):
    evaluation_managers_list = EvaluationManager.objects.all().order_by('-end_date')
    paginator = Paginator(evaluation_managers_list, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    stats = statistics()
    context = {
        'active': 'evm',
        'page_obj': page_obj,
        **stats
    }
    return render(request, 'evaluation_manager/list.html', context)


def archive_evaluation_manager(request, pk):
    manager = EvaluationManager.objects.filter(id=pk).get()
    if request.method == 'POST':
        if manager.archived:
            EvaluationManager.objects.filter(id=pk).update(archived=False)
            evaluations = Evaluation.objects.all()
            for evaluation in evaluations:
                if evaluation.course.academic_year == manager.academic_year \
                        and evaluation.course.semester == manager.semester:
                    Evaluation.objects.filter(id=evaluation.id).update(archived=False)
            messages.success(request, f"Manager and respective evaluations unarchived successfully")
            return redirect('evaluation_managers')
        else:
            EvaluationManager.objects.filter(id=pk).update(archived=True)
            evaluations = Evaluation.objects.all()
            for evaluation in evaluations:
                if evaluation.course.academic_year == manager.academic_year \
                        and evaluation.course.semester == manager.semester:
                    Evaluation.objects.filter(id=evaluation.id).update(archived=True)
            messages.success(request, f"Manager and respective evaluations archived successfully")
            return redirect('evaluation_managers')


@only_admins
def archive_evaluation_managers(request):
    archived_managers = EvaluationManager.objects.filter(archived=True)
    stats = statistics()
    context = {'page_obj': archived_managers, **stats, 'active': 'evm',}
    return render(request, 'evaluation_manager/archived_evaluation_managers.html', context)


@only_admins
def evaluation_manager_view(request, pk):
    manager = EvaluationManager.objects.filter(id=pk).first()
    evaluations = Evaluation.objects.all()
    stats = statistics()

    display_related_evaluations = []
    for evaluation in evaluations:
        if evaluation.course.academic_year == manager.academic_year \
                and evaluation.course.semester == manager.semester:
            display_related_evaluations.append(evaluation)
    paginator = Paginator(display_related_evaluations, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'page_obj': page_obj, **stats, 'manager': manager,'active': 'evm',}
    return render(request, 'evaluation_manager/evaluation_manager.html', context)


@only_admins
def create_evaluation_manager(request):
    stats = statistics()
    form = EvaluationManagerForm(request.POST or None)
    context = {'form': form, 'btn_text': 'Create', **stats}
    if form.is_valid():
        form.save()
        messages.success(request, f"Record Created successfully")
        # send notification emails to all students
        bulk = []
        em = EvaluationManager.objects.latest('id')
        students = CustomUser.objects.filter(is_student=True, is_active=True)
        for student in students:
            bulk.append(
                {
                    "Email": student.email,
                    "Name": student.first_name
                }
            )

        send_bulk_mail(bulk, f"Evaluation for Academic year {em.academic_year}:Semester {em.semester} is Opened!",
                       f"Dear Student, <br>"
                       f"<p>Please visit the QAP-Portal to evaluate your lecturers for the respective courses.</p>"
                       f"<p>Deadline for evaluation exercise is {em.end_date}.</p>"
                       f"<p>Thank you</p>"
                       f"Yours Sincerely,<br/>"
                       f"QAPD-GIMPA")

        return redirect('evaluation_managers')
    else:
        context['form'] = form

    return render(request, 'evaluation_manager/create.html', context)


@only_admins
def edit_evaluation_manager(request, pk):
    stats = statistics()
    manager = EvaluationManager.objects.filter(id=pk).first()
    form = EvaluationManagerForm(request.POST or None, instance=manager)
    context = {'form': form, 'btn_text': 'Update', **stats, 'active': 'evm',}
    if form.is_valid():
        form.save()
        messages.success(request, f"Record Updated successfully")
        return redirect('evaluation_managers')
    else:
        context['form'] = form

    return render(request, 'evaluation_manager/create.html', context)


@only_admins
def delete_evaluation_manager(request, pk):
    manager = EvaluationManager.objects.filter(id=pk).first()
    if request.method == 'POST':
        manager.delete()
        messages.success(request, f"Record Deleted successfully")

        return redirect('evaluation_managers')