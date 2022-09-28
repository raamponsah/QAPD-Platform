import datetime
import uuid

from django.db import models

# Create your models here.
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.defaultfilters import slugify
from django.utils import timezone

from core.models import Evaluation


class EvaluationManager(models.Model):
    semester_choices = (
        (1, 'First'),
        (2, 'Second'),
        (3, 'Third'),
    )
    # course = models.ForeignKey('CourseInformation', on_delete=models.CASCADE)
    academic_year = models.CharField(max_length=10, null=True, blank=True)
    semester = models.SmallIntegerField(choices=semester_choices, default=1, null=True, blank=True)
    slug = models.SlugField(unique=True, blank=True, null=True)
    start_date = models.DateField(blank=False, null=False, default=None)
    end_date = models.DateField(blank=False, null=False, default=None)
    ended = models.BooleanField(default=False)
    archived = models.BooleanField(default=False)

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Academic Year: {self.academic_year} - Semester:{self.semester}"

    def save(self, *args, **kwargs):
        self.slug = slugify(f"{self.academic_year}-{self.semester}")
        return super(EvaluationManager, self).save()

    class Meta:
        models.UniqueConstraint(fields=['academic_year','semester'], name='unique_academic_calendar')

    # @receiver(post_save, sender=Member)
    # def member_created(sender, instance, created, *args, **kwargs):


@receiver(post_save, sender=EvaluationManager)
def update_evaluation_info(sender, instance, created, *args, **kwargs):
    evaluations = Evaluation.objects.all()
    for evaluation in evaluations:
        if evaluation.course.academic_year == instance.academic_year \
                and evaluation.course.semester == instance.semester:
            Evaluation.objects.filter(id=evaluation.id).update(start_date=instance.start_date,
                                                               end_date=instance.end_date, ended=instance.ended
                                                               , archived=instance.archived)