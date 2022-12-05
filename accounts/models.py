from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.exceptions import ValidationError
from django.db import models
from qapd import settings


def validate_gimpa_email(value):
    if "gimpa.edu.gh" in value:
        return value
    else:
        raise ValidationError("Only validated GIMPA emails are allowed")


class CustomManager(BaseUserManager):

    def create_user(self, email, username, first_name, last_name, password=None, **other_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, username=username,
                          first_name=first_name, last_name=last_name, **other_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, username, first_name, last_name, password=None, **other_fields, ):
        other_fields.setdefault('is_student', False)
        other_fields.setdefault('is_lecturer', False)
        other_fields.setdefault('is_qadmin', True)
        other_fields.setdefault('is_hadmin', True)
        other_fields.setdefault('is_active', True)
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)

        return self.create_user(email, username, first_name, last_name, password, **other_fields, )


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, db_index=True, validators=[validate_gimpa_email])
    username = models.CharField(max_length=30, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    is_student = models.BooleanField(default=False)
    is_lecturer = models.BooleanField(default=False)
    is_qadmin = models.BooleanField(default=False)
    is_hadmin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    # is_active = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = CustomManager()
    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'username']

    def __str__(self):
        return self.first_name + ' ' + self.last_name

    class Meta:
        verbose_name = 'User'


class ActivateUser(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    token = models.CharField(max_length=300, blank=False, null=False)
    expiry = models.DateTimeField(blank=False, null=False)
    is_activated = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.email} - {self.is_activated}"


class LecturerProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, blank=False, null=False, on_delete=models.CASCADE,
                                related_name='lecturer')
    staff_id = models.PositiveIntegerField(default=0000)

    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name


# @receiver(signal=post_save, sender=CustomUser)
# def create_lecturer_profile(sender, instance, created, **kwargs):
#     if created and instance.is_lecturer is True:
#         return LecturerProfile.objects.create(user=instance)


class Student(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, blank=False, null=False, on_delete=models.CASCADE,
                                related_name='student')

    choices = (
        ('1', 'Year 1'),
        ('2', 'Year 2'),
        ('3', 'Year 3'),
        ('4', 'Year 4'),
    )
    # choices = (
    #     ('000', 'Diploma'),
    #     ('100', 'Level 100'),
    #     ('200', 'Level 200'),
    #     ('300', 'Level 300'),
    #     ('400', 'Level 400'),
    #     ('600', 'Level 600-PGD'),  # pgd students
    #     ('700', 'Level 700'),
    #     ('800', 'Level 800'),
    # )

    lecture_group = (
        ('day', 'Day'),
        ('evening', 'Evening'),
        ('weekend', 'Weekend'),
    )

    program = models.ForeignKey('core.ProgramInformation', blank=False, null=True, on_delete=models.SET_NULL)
    course_group = models.CharField(max_length=30, choices=lecture_group, default="day", null=True, blank=False)
    level = models.CharField(max_length=30, choices=choices, null=True, blank=False)
    campus = models.ForeignKey('core.CampusInformation', blank=False, null=True, on_delete=models.SET_NULL,
                               related_name="campus")

    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name

    class Meta:
        verbose_name = 'Student Profile'

# @receiver(signal=post_save, sender=CustomUser)
# def create_student_profile(sender, instance, created, **kwargs):
#     if created and instance.is_student is True:
#         student_profile = Student.objects.create(user=instance)
#         return student_profile


# @receiver(signal=post_save, sender=CustomUser)
# def create_lecturer_profile(sender, instance, created, **kwargs):
#     if created and instance.is_lecturer is True:
#         lecturer_profile = LecturerProfile.objects.create(user=instance)
#         return lecturer_profile