from django.db import models

# Create your models here.

class CurrencyModel(models.Model):
    prefix = models.CharField(max_length=10,blank=True,null=True)
    short_key = models.CharField(max_length=100,unique=True)
    rate = models.DecimalField(max_digits=8,decimal_places=5,default=0)
    is_active = models.BooleanField(default=True)
    
    

class PaymentGatewayModel(models.Model):
    name = models.CharField(max_length=255)
    currency = models.ForeignKey(CurrencyModel,on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)