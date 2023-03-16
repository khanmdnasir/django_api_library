from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(SMSConfigModel)
admin.site.register(SMSScheduleModel)
admin.site.register(EmailScheduleModel)
admin.site.register(NotificationSubsribe)
admin.site.register(NotificationModel)