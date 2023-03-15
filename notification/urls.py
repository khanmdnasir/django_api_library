# myproject/urls.py
from django.urls import path, include
from rest_framework import routers
from .views import *

router = routers.DefaultRouter()
router.register('sms_config', SMSConfigViewSet)
router.register('notifications', NotificationViewSet)
router.register('sms_schedule', SMSScheduleViewSet)
router.register('email_schedule', EmailScheduleViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('send_sms/',SendSMSApi.as_view()),
    path('send_sms_all/',SendSMSAllApi.as_view()),
    path('send_email/',SendEmailApi.as_view()),
    path('send_email_all/',SendEmailAllApi.as_view()),
    path('user_notifications/',UserNotificationApi.as_view()),
    path('send_notification/',SendNotificationApi.as_view()),
    path('send_notification_all/',SendNotificationAllApi.as_view()),
]