from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from django.contrib.auth import get_user_model

# Register your models here.
from django.contrib.auth.forms import UserCreationForm

from accounts.models import Student, CustomUser, LecturerProfile


# User = get_user_model()


class CustomUserAdmin(UserAdmin):
    # ordering = ('-start_date',)
    search_fields = ('email', 'last_name', 'username')
    list_display = ('email', 'username', 'first_name', 'last_name', 'is_active', 'is_staff', 'is_student', 'is_qadmin',
                    'is_lecturer', 'is_superuser')

    fieldsets = (
        (None, {'fields': ('email', 'username', 'first_name', 'last_name',)}),
        (
            'Permissions',
            {'fields': ('is_staff', 'is_active', 'is_qadmin', 'is_student', 'is_lecturer', 'is_superuser')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'first_name',
                       'last_name', 'password1', 'password2', 'is_qadmin', 'is_student',
                       'is_staff', 'is_lecturer', 'is_active', 'is_superuser')}),
    )


admin.site.register(CustomUser, CustomUserAdmin)


class LecturerProfileAdmin(admin.ModelAdmin):
    search_fields = ('staff_id',)


admin.site.register(LecturerProfile, LecturerProfileAdmin)

class StudentProfileAdmin(admin.ModelAdmin):
    search_fields = ('user',)
admin.site.register(Student, StudentProfileAdmin)