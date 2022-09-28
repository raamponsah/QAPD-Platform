from django import forms

from core.models import AcademicYear, School, Department, Program, Course, Evaluation, Facilitator


class AcademicYearForm(forms.ModelForm):
    class Meta:
        model = AcademicYear
        fields = ['academic_year']

        widgets = {
            'academic_year': forms.TextInput(attrs={'placeholder': '2021/22 Academic Year', 'class': "form-control"})
        }


class SchoolForm(forms.ModelForm):
    class Meta:
        model = School
        fields = ['name', 'description']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'School of Technology'}),
            'description': forms.Textarea(
                attrs={'class': 'form-control', 'placeholder': 'School of Technology description'}),
        }


class CreateDepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = [
            'name', 'school'
        ]

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Department of Information Sytems'}),
            'school': forms.Select(attrs={'class': 'form-control'}),
        }


class CreateProgramForm(forms.ModelForm):
    class Meta:
        model = Program
        fields = [
            'name', 'department', 'description'
        ]

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Program'}),
            'department': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(
                attrs={'class': 'form-control', 'placeholder': 'Program description'}),
        }


class CreateCourseForm(forms.ModelForm):

    class Meta:
        model = Course
        fields = [
            'name', 'program', 'course_code', 'course_group', 'level', 'description', 'facilitator'
        ]

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Course'}),
            'program': forms.Select(attrs={'class': 'form-control'}),
            'course_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'GSOT034'}),
            'course_group': forms.Select(attrs={'class': 'form-control'}),
            'level': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(
                attrs={'class': 'form-control', 'placeholder': 'Course description'}),
            'facilitator': forms.Select(attrs={'class': 'form-control'}),
            # 'slug':forms.HiddenInput()
        }


class SetupEvaluationForm(forms.ModelForm):
    class Meta:
        model = Evaluation
        fields = [
            'academic_year', 'course', 'facilitator', 'deadline', 'description'
        ]

        widgets = {
            'academic_year': forms.Select(attrs={'class': 'form-control'}),
            'course': forms.Select(attrs={'class': 'form-control'}),
            'facilitator': forms.Select(attrs={'class': 'form-control'}),
            'deadline': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'description': forms.Textarea(
                attrs={'class': 'form-control', 'placeholder': 'Course Evaluation description'}),
        }


class AddFacilitatorForm(forms.ModelForm):
    class Meta:
        model = Facilitator
        fields = [
            'first_name', 'last_name', 'staff_id', 'school'
        ]

        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Kofi'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Mensah'}),
            'staff_id': forms.NumberInput(attrs={'class': 'form-control'}),
            'school': forms.Select(attrs={'class': 'form-control'}),
        }