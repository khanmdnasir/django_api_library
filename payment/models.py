from django.db import models
from solo.models import SingletonModel
# Create your models here.

class EBLConfig(SingletonModel):
    merchantId = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    testMerchantId = models.CharField(max_length=255)
    testPassword = models.CharField(max_length=255)
    testMode = models.BooleanField(default=True)

class CurrencyModel(models.Model):
    prefix = models.CharField(max_length=10,blank=True,null=True)
    short_key = models.CharField(max_length=100,unique=True)
    rate = models.DecimalField(max_digits=8,decimal_places=5,default=0)
    is_active = models.BooleanField(default=True)
    
    

class PaymentGatewayModel(models.Model):
    name = models.CharField(max_length=255)
    currency = models.ForeignKey(CurrencyModel,on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)