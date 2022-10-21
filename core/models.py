import uuid

from django.db import models
# Create your models here.
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils import timezone

from accounts.models import Student


class CourseInformation(models.Model):
    lecture_groups = (
        ('day', 'Day'),
        ('evening', 'Evening'),
        ('weekend', 'Weekend'),
    )
    level_choices = (
        ('1', 'Year 1'),
        ('2', 'Year 2'),
        ('3', 'Year 3'),
        ('4', 'Year 4'),
    )
    # level_choices = (
    #     ('000', 'Diploma'),
    #     ('100', 'Level 100'),
    #     ('200', 'Level 200'),
    #     ('300', 'Level 300'),
    #     ('400', 'Level 400'),
    #     ('600', 'Level 600-PGD'),  # pgd students
    #     ('700', 'Level 700'),
    #     ('800', 'Level 800'),
    # )
    academic_year = models.CharField(max_length=10, null=True, blank=True)
    campus_name = models.CharField(max_length=255, null=True, blank=True)
    faculty_school_name = models.CharField(max_length=255, null=True, blank=True)
    department_name = models.CharField(max_length=255, null=True, blank=True)
    qualification_name = models.CharField(max_length=255, null=True, blank=True)
    lecturer_code = models.IntegerField(null=True, blank=True)
    subject_code = models.CharField(max_length=255, null=True, blank=True)
    subject_name = models.CharField(max_length=255, null=True, blank=True)
    semester = models.SmallIntegerField(null=True, blank=True)
    level = models.CharField(max_length=30, choices=level_choices, null=True, blank=False)
    course_group = models.CharField(max_length=255, null=True, blank=True, choices=lecture_groups)

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.subject_name} {self.lecturer_code} {self.campus_name}"

    # @property
    # def staff_name(self):
    #     return f"{self.subject_name} {self.code}"

    class Meta:
        verbose_name = 'Course Data'
        verbose_name_plural = 'Course Data'

        constraints = [
            models.UniqueConstraint(fields=[
                'academic_year', 'subject_code', 'course_group', 'campus_name', 'subject_name', 'qualification_name',
                'faculty_school_name', 'semester', 'lecturer_code', 'level', 'department_name'
            ], name='unique_classified_course')
        ]


class Evaluation(models.Model):
    course = models.ForeignKey(CourseInformation, blank=True, null=True, on_delete=models.CASCADE,
                               related_name='related_evaluation')
    slug = models.SlugField(unique=True, default=uuid.uuid4)
    start_date = models.DateTimeField(null=True, blank=True, default=None)
    end_date = models.DateTimeField(null=True, blank=True, default=None)
    archived = models.BooleanField(default=False)
    ended = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'Evaluation Reports'

    @property
    def check_active_status(self):
        if self.deadline > timezone.now():
            return True
        else:
            return False

    def __str__(self):
        return f"{self.course.subject_code} - {self.course.subject_name} "

    def save(self, *args, **kwargs):
        # slug_value = self.course.name + '-' + str(self.facilitator.staff_id) + '-' + self.course.course_group
        # self.slug = slugify(slug_value)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('evaluation_report', kwargs={'slug': self.slug})


class EvaluationSubmission(models.Model):
    class FeedbackChoices(models.IntegerChoices):
        NOT_APPLICABLE = 0
        STRONGLY_DISAGREE = 1
        DISAGREE = 2
        MODERATELY_DISAGREE = 3
        AGREE = 4
        STRONGLY_AGREE = 5

    evaluationInfo = models.ForeignKey(Evaluation, blank=True, null=True, on_delete=models.CASCADE,
                                       related_name='evaluation_form')

    curriculum_feedback_beginning_answer = models.IntegerField(choices=FeedbackChoices.choices, default=None)
    curriculum_feedback_course_answer = models.IntegerField(choices=FeedbackChoices.choices, default=None)
    curriculum_feedback_lecture_answer = models.IntegerField(choices=FeedbackChoices.choices, default=None)
    curriculum_feedback_outcomes_answer = models.IntegerField(choices=FeedbackChoices.choices, default=None)
    curriculum_feedback_procedures_answer = models.IntegerField(choices=FeedbackChoices.choices, default=None)
    curriculum_feedback_books_answer = models.IntegerField(choices=FeedbackChoices.choices, default=None)

    attendance_schedule = models.IntegerField(choices=FeedbackChoices.choices, default=None)
    attendance_punctuality = models.IntegerField(choices=FeedbackChoices.choices, default=None)
    attendance_presence = models.IntegerField(choices=FeedbackChoices.choices, default=None)

    delivery_enthusiasm = models.IntegerField(choices=FeedbackChoices.choices, default=None)
    delivery_sequence = models.IntegerField(choices=FeedbackChoices.choices, default=None)
    delivery_organization = models.IntegerField(choices=FeedbackChoices.choices, default=None)
    delivery_clarity = models.IntegerField(choices=FeedbackChoices.choices, default=None)
    delivery_contents = models.IntegerField(choices=FeedbackChoices.choices, default=None)
    delivery_responsiveness = models.IntegerField(choices=FeedbackChoices.choices, default=None)
    delivery_achievements = models.IntegerField(choices=FeedbackChoices.choices, default=None)
    delivery_innovation = models.IntegerField(choices=FeedbackChoices.choices, default=None)
    delivery_theory_practices = models.IntegerField(choices=FeedbackChoices.choices, default=None)

    assignments_relevance = models.IntegerField(choices=FeedbackChoices.choices, default=None)
    assignments_promptitude = models.IntegerField(choices=FeedbackChoices.choices, default=None)
    assignments_feedback = models.IntegerField(choices=FeedbackChoices.choices, default=None)
    assignments_guidance = models.IntegerField(choices=FeedbackChoices.choices, default=None)

    interaction_availability = models.IntegerField(choices=FeedbackChoices.choices, default=None)
    interaction_help = models.IntegerField(choices=FeedbackChoices.choices, default=None)
    interaction_fairness = models.IntegerField(choices=FeedbackChoices.choices, default=None)

    environment_classroom_size = models.IntegerField(choices=FeedbackChoices.choices, default=None)
    environment_seats = models.IntegerField(choices=FeedbackChoices.choices, default=None)
    environment_audio_visual_equip = models.IntegerField(choices=FeedbackChoices.choices, default=None)
    environment_public_address = models.IntegerField(choices=FeedbackChoices.choices, default=None)
    environment_books = models.IntegerField(choices=FeedbackChoices.choices, default=None)
    environment_computers = models.IntegerField(choices=FeedbackChoices.choices, default=None)
    environment_internet = models.IntegerField(choices=FeedbackChoices.choices, default=None)
    environment_air_conditioning = models.IntegerField(choices=FeedbackChoices.choices, default=None)
    environment_secretariat = models.IntegerField(choices=FeedbackChoices.choices, default=None)

    slug = models.SlugField(unique=True, default=uuid.uuid4)
    submitter = models.ForeignKey(Student, blank=True, null=True, on_delete=models.PROTECT)
    is_evaluated = models.BooleanField(blank=False, null=False, default=False)

    # deadline = models.DateTimeField(null=False,blank=False, default=datetime.datetime)

    def __str__(self):
        return f"{self.evaluationInfo} {self.submitter}"

    def save(self, *args, **kwargs):
        # self.slug = str(self.evaluationInfo) + '-' + str(uuid.uuid4())
        # self.slug = slugify(self.slug[50:])
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('evaluation', args=[self.slug])

    class Meta:
        unique_together = [('evaluationInfo', 'submitter')]


class ProgramInformation(models.Model):
    program_name = models.CharField(max_length=255)
    department_name = models.CharField(max_length=255)
    school = models.ForeignKey('School', blank=True, null=True, on_delete=models.PROTECT)

    def __str__(self):
        return self.program_name


class CampusInformation(models.Model):
    campus_name = models.CharField(max_length=255)

    def __str__(self):
        return self.campus_name


class School(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


@receiver(post_save, sender=CourseInformation)
def build_respective_evaluation_form(sender, instance, created, **kwargs):
    e = Evaluation.objects.filter(course=instance).first()
    if e:
        Evaluation.objects.filter(id=e.id).update(course=instance)
    else:
        Evaluation(course=instance).save()