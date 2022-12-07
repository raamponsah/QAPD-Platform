from django.contrib import messages
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.urls import reverse

from accounts.models import CustomUser


class CustomBackend(ModelBackend):

    def authenticate(self, request, **kwargs):
        email = kwargs['username']
        password = kwargs['password']
        try:
            custom_user = CustomUser.objects.get(email=email)
            if custom_user.user.check_password(password) is True:
                return custom_user.user
        except CustomUser.DoesNotExist:
            return None
            # return reverse('welcome')

    def get_user(self, user_id):
        """
        Overrides the get_user method to allow users to log in using their email address.
        """
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None