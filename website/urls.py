from django.urls import path

from website.views import website, redirect_to_welcome

urlpatterns = [
    path('welcome/', redirect_to_welcome, name='redirect_to_welcome'),
]