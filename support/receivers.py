from django.dispatch import receiver
from .models import TicketLogsModel
from . import signals


@receiver(signals.ticket_log_task)
def ticket_log_signals(sender, data, ticket, request, **kwargs):
    try:
        if data['action_types'] == 'created':
            action_creators_email = ticket.email
        else:
            action_creators_email = request.user.email
        ticket_log = TicketLogsModel.objects.create(ticket_id=ticket,action_types=data['action_types'], support_agent = ticket.support_agent,details=data['details'], ticket_status=data['status'], ticket_priority=data['priority'], action_creators_email= action_creators_email)

        ticket_log.save()

        # print("ticket_log",ticket_log)

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