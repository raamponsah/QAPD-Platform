from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from qapd import settings

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('/', include('website.urls')),
                  path('core/', include('core.urls')),
                  path('student-manager/', include('student_manager.urls')),
                  path('evaluation-managers/', include('evaluation_manager.urls')),
                  path('lecturers/', include('lecturer_portal.urls')),
                  path('computation/', include('compute.urls')),
                  path('email-service/', include('email_service.urls')),
                  path('reports/', include('reports.urls')),
                  path('accounts/', include('accounts.urls')),
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)