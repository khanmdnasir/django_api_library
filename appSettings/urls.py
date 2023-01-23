from django.urls import path
from .views import *



urlpatterns = [
    path('settings/',AppSettingsApi.as_view()),
    path('document/',DocumentApi.as_view()),
]
