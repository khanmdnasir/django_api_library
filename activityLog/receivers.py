from django.dispatch import receiver
from django.contrib.auth import user_logged_in,user_login_failed
from .models import AuthenticationLog,ActivityLog
from . import signals




def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

@receiver(user_logged_in)
def log_user_logged_in_success(sender, user, request, **kwargs):
    try:
        print('user logged in success')
        user_agent_info = request.META.get('HTTP_USER_AGENT', '<unknown>')[:255]
        user_login_activity_log = AuthenticationLog(login_IP=get_client_ip(request),
                                                    login_email=user.email,
                                                    user_agent_info=user_agent_info,
                                                    status=AuthenticationLog.SUCCESS)
        user_login_activity_log.save()
    except Exception as e:
        # log the error
        print(e)
        

@receiver(user_login_failed)
def log_user_logged_in_failed(sender, credentials, request, **kwargs):
    try:
        user_agent_info = request.META.get('HTTP_USER_AGENT', '<unknown>')[:255]
        user_login_activity_log = AuthenticationLog(login_IP=get_client_ip(request),
                                                    login_email=credentials['email'],
                                                    user_agent_info=user_agent_info,
                                                    status=AuthenticationLog.FAILED)
        user_login_activity_log.save()
    except Exception as e:
        # log the error
        print(e)

@receiver(signals.activity_log_task)
def activity_log_signals(sender, user,credentials, request, **kwargs):
    try:
        print('activity log')
        user_agent_info = request.META.get('HTTP_USER_AGENT', '<unknown>')[:255]
        activity_log = ActivityLog.objects.create(action_type=credentials['action_type'],action_model=credentials['action_model'],action_object=credentials['action_object'],
                                   action_IP=get_client_ip(request),action_user=user.email,action_agent_info=user_agent_info,
                                   )
        print(activity_log)
    except Exception as e:
        # log the error
        print(e)