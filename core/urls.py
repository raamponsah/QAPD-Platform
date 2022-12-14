from django.urls import path

from core.views import evaluations, evaluation_view_form

urlpatterns = [
    path('', evaluations, name='evaluations'),
    path('evaluate/<int:pk>/', evaluation_view_form, name='evaluation_form'),
]