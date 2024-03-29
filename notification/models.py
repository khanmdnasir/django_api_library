from django.db import models
from django.db.models.signals import post_save,post_delete
from django.dispatch import receiver
from django_celery_beat.models import PeriodicTask, CrontabSchedule
import json
from solo.models import SingletonModel
from user.models import User

# from django.core.validators import MaxValueValidator,MinValueValidator

# Create your models here.

class SMSConfigModel(SingletonModel):
    from_number = models.CharField(max_length=100)

notification_type_choices = (
    ('schedule','schedule'),
    ('broadcast','broadcast'),
    ('non_schedule','non_schedule')
)
class SMSScheduleModel(models.Model):
    receiver = models.ManyToManyField(User)
    schedule_month = models.CharField(max_length=255,default='*')
    schedule_day = models.CharField(max_length=255,default='*')
    schedule_hour = models.CharField(max_length=255,default='*')
    schedule_minute = models.CharField(max_length=255,default='*')
    text = models.TextField()
    send_to_all = models.BooleanField(default=False)
    active = models.BooleanField(default=True)


@receiver(post_save, sender=SMSScheduleModel)
def sms_handler(sender, instance, created, **kwargs):
    # call group_send function directly to send notificatoions or you can create a dynamic task in celery beat

    schedule, created = CrontabSchedule.objects.get_or_create(hour = instance.schedule_hour, minute = instance.schedule_minute, day_of_month = instance.schedule_day, month_of_year = instance.schedule_month)
    
    periodic_task = PeriodicTask.objects.filter(name="broadcast-sms-"+str(instance.id))
    if len(periodic_task) > 0:
        for ptask in periodic_task:
            ptask.update(crontab=schedule, name="broadcast-sms-"+str(instance.id), task="notification.tasks.schedule_sms_send_task", args=json.dumps((instance.id,)))

    else:
        PeriodicTask.objects.create(crontab=schedule, name="broadcast-sms-"+str(instance.id), task="notification.tasks.schedule_sms_send_task", args=json.dumps((instance.id,)))

@receiver(post_delete,sender=SMSScheduleModel)
def sms_handler_delete(sender, instance, created, **kwargs):
    periodic_task = PeriodicTask.objects.filter(name="broadcast-sms-"+str(instance.id))
    if len(periodic_task) > 0:
        for ptask in periodic_task:
            ptask.delete()

class EmailScheduleModel(models.Model):
    receiver = models.ManyToManyField(User)
    schedule_month = models.CharField(max_length=255,default='*')
    schedule_day = models.CharField(max_length=255,default='*')
    schedule_hour = models.CharField(max_length=255,default='*')
    schedule_minute = models.CharField(max_length=255,default='*')
    mail_subject = models.CharField(max_length=500)
    text = models.TextField()
    send_to_all = models.BooleanField(default=False)
    active = models.BooleanField(default=True)

    
    
@receiver(post_save, sender=EmailScheduleModel)
def email_handler(sender, instance, created, **kwargs):
    # call group_send function directly to send notificatoions or you can create a dynamic task in celery beat
    
    schedule, created = CrontabSchedule.objects.get_or_create(hour = instance.schedule_hour, minute = instance.schedule_minute, day_of_month = instance.schedule_day, month_of_year = instance.schedule_month)
    periodic_task = PeriodicTask.objects.filter(name="broadcast-email-"+str(instance.id))
    if len(periodic_task) > 0:
        for ptask in periodic_task:
            ptask.update(crontab=schedule, name="broadcast-email-"+str(instance.id), task="notification.tasks.schedule_mail_send_task", args=json.dumps((instance.id,)))
    else:   
        PeriodicTask.objects.create(crontab=schedule, name="broadcast-email-"+str(instance.id), task="notification.tasks.schedule_mail_send_task", args=json.dumps((instance.id,)))

@receiver(post_delete,sender=EmailScheduleModel)
def email_handler_delete(sender, instance, created, **kwargs):
    periodic_task = PeriodicTask.objects.filter(name="broadcast-email-"+str(instance.id))
    if len(periodic_task) > 0:
        for ptask in periodic_task:
            ptask.delete()

class NotificationModel(models.Model):
    # user_sender = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True,related_name='user_sender')
    receiver = models.ManyToManyField(User)
    notification_type = models.CharField(max_length=255,choices=notification_type_choices)
    message = models.TextField()
    broadcast_month = models.CharField(max_length=255,default='*')
    broadcast_day = models.CharField(max_length=255,default='*')
    broadcast_hour = models.CharField(max_length=255,default='*')
    broadcast_minute = models.CharField(max_length=255,default='*')
    send_to_all = models.BooleanField(default=False)
    active = models.BooleanField(default=True)


@receiver(post_save, sender=NotificationModel)
def notification_handler(sender, instance, created, **kwargs):
    # call group_send function directly to send notificatoions or you can create a dynamic task in celery beat
    
    if instance.notification_type != 'non_schedule':
        schedule, created = CrontabSchedule.objects.get_or_create(hour = instance.broadcast_hour, minute = instance.broadcast_minute, day_of_month = instance.broadcast_day, month_of_year = instance.broadcast_month)
        periodic_task = PeriodicTask.objects.filter(name="broadcast-notification-"+str(instance.id))
        if len(periodic_task) > 0:
            for ptask in periodic_task:
                ptask.update(crontab=schedule, name="broadcast-notification-"+str(instance.id), task="notification.tasks.broadcast_notification", args=json.dumps((instance.id,)))
        else:
            PeriodicTask.objects.create(crontab=schedule, name="broadcast-notification-"+str(instance.id), task="notification.tasks.broadcast_notification", args=json.dumps((instance.id,)))


@receiver(post_delete,sender=NotificationModel)
def notification_handler_delete(sender, instance, created, **kwargs):
    periodic_task = PeriodicTask.objects.filter(name="broadcast-notification-"+str(instance.id))
    if len(periodic_task) > 0:
        for ptask in periodic_task:
            ptask.delete()