from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend


class EmailBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        user = get_user_model()
        try:
            found_user = user.objects.get(email=username)
        except user.DoesNotExist:
            return None
        else:
            if found_user.check_password(password) is True:
                if found_user.is_active:
                    return user
        return None

    def get_user(self, user_id):
        User = get_user_model()
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None