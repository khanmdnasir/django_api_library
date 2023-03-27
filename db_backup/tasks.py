from celery import shared_task
from django.core import management

@shared_task(bind=True)
def db_backup_task(self):
    try:
        management.call_command('dbbackup')
        return True
    except Exception as e:
        print(str(e))
        return False