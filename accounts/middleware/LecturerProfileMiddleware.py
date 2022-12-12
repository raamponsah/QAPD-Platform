from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse

from accounts.models import LecturerProfile


def lpm(get_response):
    def middleware(request):
        response = get_response(request)
        try:
            if request.user.id is not None and request.user.is_lecturer is True:
                LecturerProfile.objects.filter(user=request.user).get()
        except LecturerProfile.DoesNotExist:
            while not (request.path == reverse('setup-lecturer-profile', kwargs={'user_id': request.user.id})):
                return redirect(reverse('setup-lecturer-profile', kwargs={'user_id': request.user.id}))
        return response

    return middleware