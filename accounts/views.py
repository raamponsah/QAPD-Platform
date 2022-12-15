import datetime

from django.contrib import messages
# Create your views here.
from django.contrib.auth import get_user_model
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import BadHeaderError
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from .auth_decorators import only_lecturer, only_student
from .auth_funcs import decode_token, generate_confirmation_token
from .email import generate_confirmation_link_mail, send_mail
from .forms import StudentRegisterForm, StudentProfileForm, LecturerProfileForm, LecturerRegistrationForm
from .models import LecturerProfile, ActivateUser, CustomUser

# Register your models here.
User = get_user_model()


def register_lecturer(request):
    form = LecturerRegistrationForm()
    auth_page_url = 'login_lecturer'
    auth_page_link_text = 'Have an account?'
    view_name = 'lecturer_view'
    if request.method == 'POST':
        form = LecturerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            token = generate_confirmation_token(user)
            link = f"{get_current_site(request)}/accounts/confirm-email/{token}"
            generate_confirmation_link_mail(user.email, user.username, link,
                                            extra={'password': form.cleaned_data.get('password1')})
            messages.success(request, f'A confirmation email was sent to {user.email}.\n'
                                      f'Please check your inbox or spam to continue with the registration.\n'
                             )
            return redirect('login_lecturer')
        else:
            form = LecturerRegistrationForm(request.POST)
    context = {"form": form, 'view_name': view_name, 'auth_page_url': auth_page_url,
               'auth_page_link_text': auth_page_link_text}
    return render(request, 'registration/register.html', context)


@only_lecturer
def setup_lecturer_profile(request, user_id):
    user = CustomUser.objects.get(id=user_id)
    form = LecturerProfileForm(request.POST or None, initial={'user': user_id})
    context = {'form': form, 'page_title': 'Update Profile'}
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, f"Lecturer Profile has been setup successfully")
            return redirect('lecturer_dashboard')
        else:
            context['form'] = form
            context['error'] = form.errors.as_json()
    return render(request, 'registration/setup_lecturer_profile.html', context)


@only_lecturer
def lecturer_profile_create(request, pk):
    lecturer = get_object_or_404(LecturerProfile, pk=pk)
    form = LecturerProfileForm(instance=lecturer)
    context = {
        'form': form,
        'page_title': 'Update Profile'
    }
    if request.method == 'POST':
        form = LecturerProfileForm(request.POST, instance=lecturer)
        if form.is_valid():
            form.save()
            return redirect('lecturer_dashboard')
        else:
            context['error'] = form.errors.as_json()
            return render(request, 'registration/setup_lecturer_profile.html', context)
    return render(request, 'registration/setup_lecturer_profile.html', context)


def register_student(request):
    form = StudentRegisterForm()
    auth_page_url = 'login_student'
    auth_page_link_text = 'Have an account?'
    view_name = "student_view"
    if request.method == 'POST':
        form = StudentRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            token = generate_confirmation_token(user)
            link = f"{get_current_site(request)}/accounts/confirm-email/{token}"
            generate_confirmation_link_mail(user.email, user.username, link, extra={'password': form.cleaned_data.get('password1')})
            messages.success(request, f'A confirmation email was sent to {user.email}.\n'
                                      f'Please check your inbox or spam to continue with the registration.\n'
                             )
            return redirect('login_student')
        else:
            form = StudentRegisterForm(request.POST)
    context = {"form": form, 'view_name': view_name, 'auth_page_url': auth_page_url,
               'auth_page_link_text': auth_page_link_text}
    return render(request, 'registration/register.html', context)


@only_student
def student_profile_create(request, pk):
    student = get_object_or_404(CustomUser, pk=pk)
    # print(request.user.is_authenticated, pk)
    form = StudentProfileForm(request.POST or None, initial={'user': student.id})
    context = {
        'form': form,
        'page_title': 'Create Profile'
    }
    if request.method == 'POST':
        form = StudentProfileForm(request.POST)

        if form.is_valid():
            print(request.POST)
            form.save()
            return redirect('evaluations', user_id=pk)
        else:
            print(form.errors.as_json())
            context['error'] = form.errors.as_json()
            return render(request, 'registration/register-extra.html', context)
    return render(request, 'registration/register-extra.html', context)


def login_administrator(request):
    page_title = 'Admin Login/Register'
    view_name = 'administrator'
    context = {'page_title': page_title,
               'bg': 'bg-dark',
               'admin-templates': True,
               'view_name': view_name
               }

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        # this would have to become a custom user (e.g. student)
        found_user = authenticate(username=username, password=password)
        if found_user is not None and found_user.is_qadmin is True:
            login(request, found_user)
            messages.success(request, 'Welcome ')
            return redirect('dashboard')
        else:
            context['login_error'] = 'Username or password is incorrect.'
            messages.error(request, 'Login error, credentials invalid')
            return render(request, 'accounts/auth/administrator-login.html', context)

    return render(request, 'accounts/auth/administrator-login.html', context)


def login_lecturer(request):
    page_title = 'Lecturer Login/Register'
    auth_page_url = 'register_lecturer'
    auth_page_link_text = 'No account?'
    view_name = 'lecturer_view'
    context = {'page_title': page_title,
               'bg': 'bg-dark',
               'admin-templates': True,
               'view_name': view_name,
               'auth_page_url': auth_page_url,
               'auth_page_link_text': auth_page_link_text
               }

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        # this would have to become a custom user (e.g. student)
        found_user = authenticate(username=username, password=password)
        if found_user is not None and found_user.is_lecturer is True and found_user.is_active is True:
            login(request, found_user)
            messages.success(request, f'Welcome, {found_user}')
            return redirect('lecturer_dashboard')
        else:
            context['login_error'] = 'Username or password is incorrect.'
            messages.error(request, 'Login error, credentials invalid')
            return render(request, 'accounts/auth/lecturer-login.html', context)

    return render(request, 'accounts/auth/lecturer-login.html', context)


def login_student(request):
    page_title = 'Login/Register'
    auth_page_url = 'register_student'
    auth_page_link_text = 'No Account?'
    view_name = 'student_view'
    context = {'page_title': page_title,
               'auth_page_url': auth_page_url,
               'auth_page_link_text': auth_page_link_text,
               'view_name': view_name
               }
    if request.method == "POST":
        username = request.POST['username'].strip()
        password = request.POST['password']

        # this would have to become a custom user (e.g. student)
        student = authenticate(username=username, password=password)
        if student is not None and student.is_student is True and student.is_active is True:
            login(request, student)
            messages.success(request, f'Welcome {student}')
            return redirect('evaluations', user_id=student.id)
        else:
            context['login_error'] = 'Username or password is incorrect.'
            messages.error(request, 'Login error, credentials invalid')
            return render(request, 'accounts/auth/auth_login_boxed.html', context)

    return render(request, 'accounts/auth/auth_login_boxed.html', context)


def logout_student(request):
    logout(request)
    return redirect('login_student')


def logout_lecturer(request):
    logout(request)
    return redirect('login_lecturer')


def logout_administrator(request):
    logout(request)
    return redirect('login_administrator')


def sent_confirm_view(request, email):
    context = {'message': f'A confirmation email link has been sent to your email'}
    return render(request, 'accounts/sent_confirmation_link.html', context)


def confirm_email_view(request, token):
    # decode token
    text = decode_token(token)
    url_user_email = text.split('/')[0]
    token_expiry = text.split('/')[1]
    activate_user = ActivateUser.objects.filter(token=token).get()
    if activate_user is not None:
        # ata '2022-04-29 16:45:35.242299
        if datetime.datetime.now() < datetime.datetime.strptime(token_expiry, '%Y-%m-%d %H:%M:%S.%f'):
            if activate_user.user.email == url_user_email:
                user = User.objects.filter(email=url_user_email).get()
                user.is_active = True
                activate_user.is_activated = True
                activate_user.save()
                user.save()
                messages.success(request, f"Email was confirmed successfully")
                print("user activated!")

                if user.is_lecturer:
                    return redirect('login_lecturer')
                elif user.is_student:
                    return redirect('login_student')

    return None


def user_account(request):
    user = User.objects.get(id=request.user.id)
    user_account_data = UserAccount.objects.filter(user=user).get()
    user_account_form = UserAccountForm(instance=user_account_data)
    if request.method == 'POST':
        user_account_form = UserAccountForm(request.POST or None, request.FILES, instance=user_account_data)
        if user_account_form.is_valid():
            user_account_form.save()
            messages.success(request, f"Account Updated Successfully")
            return redirect('user_account')
    context = {'form': user_account_form}
    return render(request, 'accounts/user-account.html', context)


def setup_student_profile(request, user_id):
    user = CustomUser.objects.get(id=user_id)
    form = StudentProfileForm(request.POST or None, initial={'user': user_id})
    context = {'form': form, 'page_title': 'Update Profile'}
    if request.method == 'POST':
        print(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f"Student Profile has been setup successfully")
            return redirect('evaluations', user_id=user_id)
        else:
            context['form'] = form
            context['error'] = form.errors.as_json()

    return render(request, 'registration/setup_student_profile.html', context)


def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "main/password/password_reset_email.txt"
                    c = {
                        "email": user.email,
                        'domain': '127.0.0.1:8000',
                        'site_name': 'Website',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(user.email, user.username, 'Password Reset', email)
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    return redirect("/password_reset/done/")
    password_reset_form = PasswordResetForm()
    return render(request=request, template_name="main/password/password_reset.html",
                  context={"password_reset_form": password_reset_form})