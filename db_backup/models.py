from solo.models import SingletonModel
from django.db import models
from django.db.models.signals import post_save,post_delete
from django.dispatch import receiver
from django_celery_beat.models import PeriodicTask, CrontabSchedule
import json

# Create your models here.
class DbBackupModel(SingletonModel):
    schedule_month = models.CharField(max_length=255,default='*')
    schedule_day = models.CharField(max_length=255,default='*')
    schedule_hour = models.CharField(max_length=255,default='*')
    schedule_minute = models.CharField(max_length=255,default='*')
    active = models.BooleanField(default=True)

    
    
@receiver(post_save, sender=DbBackupModel)
def db_backup_handler(sender, instance, created, **kwargs):
    # call group_send function directly to send notificatoions or you can create a dynamic task in celery beat
    
    schedule, created = CrontabSchedule.objects.get_or_create(hour = instance.schedule_hour, minute = instance.schedule_minute, day_of_month = instance.schedule_day, month_of_year = instance.schedule_month)
    periodic_task = PeriodicTask.objects.filter(name="db-backup").first()
    if periodic_task:
        if instance.active:
            periodic_task.update(crontab=schedule, name="db-backup", task="db_backup.tasks.db_backup_task")
        else:
            periodic_task.delete()
    else: 
        if instance.active:  
            PeriodicTask.objects.create(crontab=schedule, name="db-backup", task="db_backup.tasks.db_backup_task")

@receiver(post_delete,sender=DbBackupModel)
def db_backkup_handler_delete(sender, instance, created, **kwargs):
    periodic_task = PeriodicTask.objects.filter(name="db-backup").first()
    if periodic_task:
        periodic_task.delete()