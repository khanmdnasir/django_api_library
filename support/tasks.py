from celery import shared_task
from .models import TicketModel
from .serializers import TicketLogsSerializer, TicketLogsModel, TicketSerializer
from django.contrib.auth import get_user_model
from main import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from channels.layers import get_channel_layer
import asyncio, json
from asgiref.sync import async_to_sync
from celery.exceptions import Ignore


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



@shared_task(bind=True)
def sendTicketToWebSocket(self, socketReceiversData, ticketData, **kwargs):
    channel_layer = get_channel_layer()
    
    async def send_ticket(group_name, room_name, ticketData):
        try:
            group_room_name = "ticket_"+str(group_name)+'_'+str(room_name)

            await (channel_layer.group_send(
                group_room_name,
                {
                    'type': 'send_ticket_data',
                    'message': ticketData,
                }
            ))
        except Exception as e:
            print("Error sending ticket to websocket: {}".format(str(e)))


    async def send_all_ticket_receiver():
        tasks = []
        for key, value in socketReceiversData.items():
            if value:
                try:
                    # await send_ticket(key, value, ticketData)
                    task = asyncio.ensure_future(send_ticket(key, value, ticketData))
                    tasks.append(task)
                except Exception as e:
                    print('ensure_future ', str(e))
        await asyncio.gather(*tasks)
    
    
    try:

        try:
            # async_to_sync(send_all_ticket_receiver)()
            asyncio.run(send_all_ticket_receiver())
        except Exception as e:
            print("looping section error: ", str(e))

        return True

    except Exception as e:
        print("hello error", str(e))
        return False



@shared_task(bind = True)
def sendTicketDetailsToWebSocket(self, ticketDetailsData):
    
    try:
        if ticketDetailsData:
            channel_layer = get_channel_layer()
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(channel_layer.group_send(
                "ticket_details_"+str(ticketDetailsData['id']),
                {
                    'type': 'send_ticket_data',
                    'message': ticketDetailsData,
                }))

        else:
            self.update_state(
                state = 'FAILURE',
                meta = {'exe': "Not Found"}
            )

            raise Ignore()

    except Exception as e:
        print(str(e))
        self.update_state(
                state = 'FAILURE',
                meta = {'exe': "Failed"})

        raise Ignore()



@shared_task(bind = True)
def sendTicketCommentToWebSocket(self, comment):
    
    try:
        if comment:
            channel_layer = get_channel_layer()
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            ticket_id = comment['ticket_id']
            loop.run_until_complete(channel_layer.group_send(
                "ticket_comments_"+str(ticket_id),
                {
                    'type': 'send_comment_data',
                    'message': comment,
                }))

        else:
            self.update_state(
                state = 'FAILURE',
                meta = {'exe': "Not Found"}
            )

            raise Ignore()

    except Exception as e:
        print(str(e))
        self.update_state(
                state = 'FAILURE',
                meta = {'exe': "Failed"})

        raise Ignore()
