from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from user.views import *



urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('user.urls')),
    path('api/', include('appSettings.urls')),
    path('api/', include('activityLog.urls')),
    path('api/', include('notification.urls')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) +static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

