from django.urls import path

from evaluation_manager.views import evaluation_manager_view, evaluation_managers_view, \
    create_evaluation_manager, edit_evaluation_manager, delete_evaluation_manager, archive_evaluation_manager, \
    archive_evaluation_managers

urlpatterns = [
    path('', evaluation_managers_view, name='evaluation_managers'),
    path('<int:pk>/', evaluation_manager_view, name='evaluation_manager'),
    path('create/', create_evaluation_manager, name='create_evaluation_manager'),
    path('edit/<int:pk>', edit_evaluation_manager, name='edit_evaluation_manager'),
    path('delete/<int:pk>', delete_evaluation_manager, name='delete_evaluation_manager'),
    path('archive-evaluations/', archive_evaluation_managers, name='archive_evaluation_managers'),
    path('archive-evaluation/<int:pk>', archive_evaluation_manager, name='archive_evaluation_manager'),
]