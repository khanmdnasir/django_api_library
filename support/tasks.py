from celery import shared_task
from .models import TicketLogsModel, TicketModel
from django.contrib.auth import get_user_model

User = get_user_model()


@shared_task(bind=True)
def storeTicketLog(self, data, **kwargs):
    try:
        # print('data',data)
        if data['action_types'] == 'created':
                action_creators_email = data['email']
        else:
            action_creators_email = data['action_creators_email']

        data['support_agent'] = User.objects.get(pk=data['support_agent']['id']) if data['support_agent'] is not None else None

        ticket_instance = TicketModel.objects.get(pk=data['id'])
        
        ticket_log = TicketLogsModel.objects.create(
            ticket_id=ticket_instance,
            action_types=data['action_types'], 
            support_agent=data['support_agent'],
            details=data['details'],
            ticket_status=data['status'],
            ticket_priority=data['priority'],
            action_creators_email=action_creators_email)
        
        ticket_log.save()

        return True
    except Exception as e:
        print("hello error", str(e))
        return False