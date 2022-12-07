from django.urls import path

from website.views import website

urlpatterns = [
    path('welcome/', redirect_to_welcome, name='welcome'),
]