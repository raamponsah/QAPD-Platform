from django.urls import path, re_path, include

from accounts.views import student_profile_create, logout_student, register_student, login_student, \
    login_administrator, logout_administrator, register_lecturer, lecturer_profile_create, login_lecturer, \
    confirm_email_view, sent_confirm_view, user_account, setup_lecturer_profile, setup_student_profile, \
    password_reset_request

from django.contrib.auth import views as auth_views  # import this

urlpatterns = [
    path('login/student/', login_student, name="login_student"),
    path('register/student/', register_student, name="register_student"),
    path('login/lecturer/', login_lecturer, name="login_lecturer"),
    path('register/lecturer/', register_lecturer, name="register_lecturer"),
    path('login/adminstrator/', login_administrator, name="login_administrator"),
    path('profile/student/<int:pk>/create/', student_profile_create, name="student_profile_create"),
    path('profile/lecturer/<int:pk>/create/', lecturer_profile_create, name="lecturer_profile_create"),
    path('logout-student/', logout_student, name="logout_student"),
    path('logout-administrator/', logout_administrator, name="logout_administrator"),
    # path('profile/<pk:pk>', student_profile, name="student_profile"),
    path('confirm-email/<str:token>', confirm_email_view, name='confirm-view'),
    path('go-confirm-email/', sent_confirm_view, name='confirmation-message-view'),
    path('user-account/me', user_account, name='user_account'),

    # password resets process urls
    # path('password/', include('django.contrib.auth.urls')),
    path('password/reset', password_reset_request, name='password_reset_request'),


    path('setup-lecturer-profile/lecturer/<int:user_id>/', setup_lecturer_profile, name="setup-lecturer-profile"),
    path('setup-student-profile/student/<int:user_id>/', setup_student_profile, name="setup-student-profile"),
]