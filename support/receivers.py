from django.dispatch import receiver
from .models import TicketLogsModel
from . import signals


@receiver(signals.ticket_log_task)
def ticket_log_signals(user, data, request, **kwargs):
    try:

        ticket_log = TicketLogsModel.objects.create(action_type=data['action_type'],action_model=data['action_model'],action_object=data['action_object'],action_user=user.email,action_agent_info='user_agent_info',)

        print("ticket_log",ticket_log)

    except Exception as e:
        # log the error
        print(e)


@receiver(signals.ticket_email_send_task)
def email_send_signals(sender, receivers, data, template=None, **kwargs):
    try:
        pass
        # send email

    except Exception as e:
        # log the error
        print(e)


@receiver(signals.ticket_comments_task)
def ticket_comments_signals(sender, receivers, data, template=None, **kwargs):
    try:
        pass
        # send live comments

    except Exception as e:
        # log the error
        print(e)