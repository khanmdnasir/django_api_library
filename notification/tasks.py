from celery import shared_task
from user.models import User
from .helpers.helper import send_sms
from django.core.mail import EmailMultiAlternatives
from .models import SMSConfigModel
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
        notification = NotificationModel.objects.get(id = int(instance))
        print(notification.message)
        if notification:
            if notification.active:
                channel_layer = get_channel_layer()
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                loop.run_until_complete(channel_layer.group_send(
                    "notification_"+notification.id,
                    {
                        'type': 'send_notification',
                        'message': json.dumps(notification.message),
                    }))
                if notification.notification_type == 'broadcast':
                    notification.delete()
                return 'Done'
            else:
                print('Not Active')
                pass

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
                meta = {
                        'exe': "Failed"
                        # 'exc_type': type(ex).__name__,
                        # 'exc_message': traceback.format_exc().split('\n')
                        # 'custom': '...'
                    }
            )

        raise Ignore()

@shared_task(bind = True)
def non_schedule_notification(self,message,users):
    
    try:
        notification = NotificationModel.objects.create(notification_type='non_schedule',message=message,receiver=users)
        if notification:
            
            channel_layer = get_channel_layer()
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(channel_layer.group_send(
                "notification_"+notification.id,
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
        sms_config = SMSConfigModel.objects.get()
        if sms_config.send_to_all:
            users = User.objects.all()
        else:
            users = smsData.receiver

        if smsData.active:
            for u in users:
                send_sms({'to_number':u.phone,'from_number':sms_config.from_number,'body':smsData.text})
        return True
    except Exception as e:
        print(str(e))
        return False

@shared_task(bind=True)
def non_schedule_sms_send_task(self,text,users):
    try:
        sms_config = SMSConfigModel.objects.get()
        for u in users:
            send_sms({'to_number':u.phone,'from_number':sms_config.from_number,'body':text})
        return True
    except Exception as e:
        print(str(e))
        return False

@shared_task(bind=True)
def schedule_mail_send_task(self,instance):
        mailData = EmailScheduleModel.objects.get(id=int(instance))
        mail_subject = mailData.mail_subject
        text_content = mailData.text        
        html_content = f"<p>{text_content}</p>" 
        try:
            if mailData.active:
                if mailData.send_to_all:
                    users = User.objects.all()
                else:
                    users = mailData.receiver

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
def non_schedule_mail_send_task(self,mailData,users):
        
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

