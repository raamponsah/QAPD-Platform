from django import template

from accounts.models import Student, LecturerProfile
from core.models import CourseInformation, CampusInformation, ProgramInformation, EvaluationSubmission, Evaluation

register = template.Library()


@register.filter
def number_of_students_registered_per_this_course(value):
    # we need students registered for this course
    # students = CustomUser.objects.filter(is_student=True).count()
    course = CourseInformation.objects.filter(id=value).first()
    campus = CampusInformation.objects.filter(campus_name=course.campus_name).first()
    program = ProgramInformation.objects.filter(program_name=course.qualification_name).first()

    number_of_students_registered = Student.objects.filter(level=course.level, course_group=course.course_group,
                                                           campus=campus, program=program).count()
    return number_of_students_registered


@register.filter
def number_of_evaluations(value):
    course = CourseInformation.objects.filter(id=value).get()
    course_evaluation = Evaluation.objects.filter(course=course).get()
    number_of_evaluated_submissions = EvaluationSubmission.objects.filter(evaluationInfo=course_evaluation,
                                                                          is_evaluated=True).count()
    return number_of_evaluated_submissions