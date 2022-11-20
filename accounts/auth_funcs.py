import os

from cryptography.fernet import Fernet

from accounts.models import ActivateUser
from qapd import settings
from datetime import datetime, timedelta
from django.utils import timezone
import pytz
from django.utils.timezone import make_aware

# Using current time
ini_time_for_now = timezone.now()

future_date_after_7days = ini_time_for_now + \
                          timedelta(days=settings.EMAIL_CONFIRMATION_PERIOD_DAYS)


def generate_confirmation_token(user):
    key = os.getenv('CONFIRM_KEY')

    f = Fernet(key)
    user_email = user.email
    expiry = future_date_after_7days
    t = f"{user_email}/{expiry}"
    b = bytes(t, encoding='utf-8')
    token = f.encrypt(b)
    decoded_token = token.decode('utf-8')
    ActivateUser.objects.create(user=user, token=decoded_token, expiry=expiry)
    return decoded_token


def decode_token(token):
    b = bytes(token, encoding='utf-8')
    key = os.getenv('CONFIRM_KEY')
    f = Fernet(key)
    text = f.decrypt(b)
    text = text.decode('utf-8')
    return text