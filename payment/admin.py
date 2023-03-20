from django.contrib import admin
from .models import *
from import_export.admin import ImportExportMixin

# Register your models here.
admin.site.register(CurrencyModel)
admin.site.register(PaymentGatewayModel)

class OrderAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ['amount', 'customer_name', 'status']

admin.site.register(OrderModel,OrderAdmin)
