from django.db import models
from user.models import User
# Create your models here.

class ActionType(models.Model):
    name = models.CharField(max_length=255,unique=True)

    def __str__(self):
        return self.name


class AuthenticationLog(models.Model):
    # Login Status
    SUCCESS = 'S'
    FAILED = 'F'

    LOGIN_STATUS = ((SUCCESS, 'Success'),
                           (FAILED, 'Failed'))

    login_IP = models.GenericIPAddressField(null=True, blank=True)
    login_datetime = models.DateTimeField(auto_now=True)
    login_email = models.CharField(max_length=40, null=True, blank=True)
    status = models.CharField(max_length=1, default=SUCCESS, choices=LOGIN_STATUS, null=True, blank=True)
    user_agent_info = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'user_login_activity'
        verbose_name_plural = 'user_login_activities'


class ActivityLog(models.Model):
    action_type = models.CharField(max_length=255,null=True)
    action_model = models.CharField(max_length=255,null=True)
    action_object = models.PositiveIntegerField()
    action_user = models.CharField(max_length=40, null=True, blank=True)
    action_IP = models.GenericIPAddressField(null=True, blank=True)
    action_datetime = models.DateTimeField(auto_now=True)
    action_agent_info = models.CharField(max_length=255,null=True)