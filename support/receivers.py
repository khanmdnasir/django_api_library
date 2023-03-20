from django.dispatch import receiver
from . import signals
from .tasks import storeTicketLog
from celery.result import TimeoutError

@receiver(signals.ticket_log_task)
def ticket_log_signals(sender, data, **kwargs):
    try:
        result = storeTicketLog.delay(data)
        try:
            status = result.get(timeout=10)
            print("status",status)
        except TimeoutError:
            status = None
            print("status",status)

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