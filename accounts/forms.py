from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

from accounts.models import Student, LecturerProfile

User = get_user_model()


class StudentRegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=100,
                                 required=True,
                                 widget=forms.TextInput(attrs={
                                     'class': 'form-control',
                                 }))
    last_name = forms.CharField(max_length=100,
                                required=True,
                                widget=forms.TextInput(attrs={
                                    'class': 'form-control',
                                }))

    password1 = forms.CharField(max_length=50,
                                required=True,
                                widget=forms.PasswordInput(attrs={
                                    'class': 'form-control',
                                    'data-toggle': 'password',
                                    'id': 'password',
                                }))
    password2 = forms.CharField(max_length=50,
                                required=True,
                                widget=forms.PasswordInput(attrs={
                                    'class': 'form-control',
                                    'data-toggle': 'password',
                                    'id': 'password',
                                }))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password1', 'password2']

        widgets = {
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),

        }

    def save(self, commit=True):
        user = super().save(False)
        user.email = self.cleaned_data['email'].lower()
        user.is_student = True
        user.save()
        return user


class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = "__all__"

        widgets = {
            'level': forms.Select(attrs={'class': 'form-control'}),
            'course_group': forms.Select(attrs={'class': 'form-control'}),
            'program': forms.Select(attrs={'class': 'form-control'}),
            'campus': forms.Select(attrs={'class': 'form-control'}),
            'user': forms.HiddenInput(),
        }


class LecturerRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=100,
                                 required=True,
                                 widget=forms.TextInput(attrs={
                                     'class': 'form-control',
                                 }))
    last_name = forms.CharField(max_length=100,
                                required=True,
                                widget=forms.TextInput(attrs={
                                    'class': 'form-control',
                                }))

    password1 = forms.CharField(max_length=50,
                                required=True,
                                widget=forms.PasswordInput(attrs={
                                    'class': 'form-control',
                                    'data-toggle': 'password',
                                    'id': 'password',
                                }))
    password2 = forms.CharField(max_length=50,
                                required=True,
                                widget=forms.PasswordInput(attrs={
                                    'class': 'form-control',
                                    'data-toggle': 'password',
                                    'id': 'password',
                                }))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password1', 'password2']

        widgets = {
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),

        }

    def save(self, commit=True):
        user = super().save(False)
        user.is_lecturer = True
        user.is_active = False
        user.email = self.cleaned_data['email'].lower()
        user.save()
        return user


class LecturerProfileForm(forms.ModelForm):
    class Meta:
        model = LecturerProfile
        fields = "__all__"

        widgets = {
            'staff_id': forms.NumberInput(attrs={'min': '999', 'max': '9999', 'class': 'form-control', 'placeholder':'1234'}),
            'user': forms.HiddenInput(),
            # 'course_group': forms.Select(attrs={'class': 'form-control'}),
            # 'program': forms.Select(attrs={'class': 'form-control'}),
            # 'campus': forms.Select(attrs={'class': 'form-control'}),
            # 'user': forms.HiddenInput(),
        }


class CustomPasswordResetForm(forms.Form):
    # email = forms.EmailField()
    pass