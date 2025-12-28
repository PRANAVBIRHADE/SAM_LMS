from django.contrib import admin
from django.urls import path, include
from theme.views import home
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('api-auth/', include('rest_framework.urls')),
    path('users/', include('users.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('courses/', include('courses.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
