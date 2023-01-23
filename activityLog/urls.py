from django.urls import path,include
from .views import *
from rest_framework import routers


router = routers.DefaultRouter()
router.register('action_type',ActionTypeViewSet)



urlpatterns = [
    path('', include(router.urls)),
    path('activity_log/',ActivityLogApi.as_view()),
    path('auth_log/',AuthenticationLogApi.as_view()),
    
]