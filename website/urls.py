from django.urls import path

from website.views import website

urlpatterns = [
    path('welcome/', website, name='welcome'),
]