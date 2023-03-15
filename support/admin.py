from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(IssueTypesModel)
admin.site.register(TicketModel)
admin.site.register(TicketCommentsModel)
admin.site.register(TicketLogsModel)