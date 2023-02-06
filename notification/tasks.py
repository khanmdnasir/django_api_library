from celery import shared_task
from user.models import User
from .helpers.helper import send_sms
from django.core.mail import EmailMultiAlternatives
from appSettings.models import SMSConfigModel
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import *
import json
from celery import Celery, states
from celery.exceptions import Ignore
import asyncio
from main import settings

@shared_task(bind = True)
def broadcast_notification(self, instance):
    
    try:
        notification = NotificationModel.objects.filter(id = int(instance))
        if len(notification)>0:
            notification = notification.first()
            channel_layer = get_channel_layer()
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(channel_layer.group_send(
                "notification_broadcast",
                {
                    'type': 'send_notification',
                    'message': json.dumps(notification.message),
                }))
            notification.sent = True
            notification.save()
            return 'Done'

        else:
            self.update_state(
                state = 'FAILURE',
                meta = {'exe': "Not Found"}
            )

            raise Ignore()

    except:
        self.update_state(
                state = 'FAILURE',
                meta = {
                        'exe': "Failed"
                        # 'exc_type': type(ex).__name__,
                        # 'exc_message': traceback.format_exc().split('\n')
                        # 'custom': '...'
                    }
            )

        raise Ignore()

        
@shared_task(bind=True)
def schedule_sms_send_task(self,instance):
    try:
        smsData = SMSScheduleModel.objects.get(id = int(instance))
        users = User.objects.all()
        sms_config = SMSConfigModel.objects.get()
        for u in users:
            send_sms({'to_number':u.phone,'from_number':sms_config.from_number,'body':smsData.text})
        return True
    except Exception as e:
        print(str(e))
        return False

@shared_task(bind=True)
def non_schedule_sms_send_task(self,text):
    try:
        sms_config = SMSConfigModel.objects.get()
        users = User.objects.all()
        for u in users:
            send_sms({'to_number':u.phone,'from_number':sms_config.from_number,'body':text})
        return True
    except Exception as e:
        print(str(e))
        return False

@shared_task(bind=True)
def schedule_mail_send_task(self,instance):
        mailData = EmailScheduleModel.objects.get(id=int(instance))
        users = User.objects.all()
        mail_subject = mailData.mail_subject
        text_content = mailData.text        
        html_content = f"<p>{text_content}</p>" 
        try:
            for u in users:
                email = EmailMultiAlternatives(
                    mail_subject, text_content, settings.HOST_EMAIL_ADDRESS, [u.email])
                email.attach_alternative(html_content, "text/html")
                # email.attach_file(invoice['file_path'])
                email.send()
            return True
        except Exception as e:
            print(e)
            return False

@shared_task(bind=True)
def non_schedule_mail_send_task(self,instance,mailData):
        
        users = User.objects.all()
        mail_subject = mailData.mail_subject
        text_content = mailData.text        
        html_content = f"<p>{text_content}</p>" 
        try:
            for u in users:
                email = EmailMultiAlternatives(
                    mail_subject, text_content, settings.HOST_EMAIL_ADDRESS, [u.email])
                email.attach_alternative(html_content, "text/html")
                # email.attach_file(invoice['file_path'])
                email.send()
            return True
        except Exception as e:
            print(e)
            return False

