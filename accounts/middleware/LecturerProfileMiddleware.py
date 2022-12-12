from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse

from accounts.models import LecturerProfile, CustomUser


def lpm(get_response):
    def middleware(request):
        response = get_response(request)
        lecturer = CustomUser.objects.get(id=request.user.id)
        print("from lecturer router => ", lecturer)
        try:
            if lecturer is not None and lecturer.is_lecturer is True and lecturer.is_active is True:
                return response
        except LecturerProfile.DoesNotExist:
            while not (request.path == reverse('setup-lecturer-profile', kwargs={'user_id': request.user.id})):
                return redirect(reverse('setup-lecturer-profile', kwargs={'user_id': request.user.id}))
    return middleware