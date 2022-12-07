from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from qapd import settings
from website.views import website, redirect_to_welcome

urlpatterns = [
                  path('', website, name='welcome'),
                  path('welcome/', redirect_to_welcome, name='redirect_to_welcome'),
                  path('admin/', admin.site.urls),
                  path('accounts/', include('accounts.urls')),
                  path('core/', include('core.urls')),
                  path('student-manager/', include('student_manager.urls')),
                  path('evaluation-managers/', include('evaluation_manager.urls')),
                  path('lecturers/', include('lecturer_portal.urls')),
                  path('computation/', include('compute.urls')),
                  path('email-service/', include('email_service.urls')),
                  path('reports/', include('reports.urls')),
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)