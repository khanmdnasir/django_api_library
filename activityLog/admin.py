from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(ActionType)
admin.site.register(AuthenticationLog)
admin.site.register(ActivityLog)