from django.contrib import admin
from .models import *


# Register your models here.
admin.site.register(CurrencyModel)
admin.site.register(PaymentGatewayModel)
admin.site.register(OrderModel)
