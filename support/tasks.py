from celery import shared_task
from .models import TicketModel
from .serializers import TicketLogsSerializer, TicketLogsModel
from django.contrib.auth import get_user_model
from main import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

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


@shared_task(bind=True)
def ticketEmailSend(self, mailData):

    subject = mailData['subject']
    text_content = mailData['content']
    # We can use email_template or content. Here we use content
    # email_template = render_to_string(mailData['template_path'], {'name': "name", 'content': "content"})
    html_content = f"<p>{text_content}</p>"
    try:
        for u in mailData['users']:
            email = EmailMultiAlternatives(
                subject, text_content, settings.HOST_EMAIL_ADDRESS, [u])
            email.attach_alternative(html_content, "text/html")
            # email.attach_file(invoice['file_path'])
            email.send()
        return True
    except Exception as e:
        print(e)
        return False