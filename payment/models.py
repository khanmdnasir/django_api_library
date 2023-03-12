from django.db import models

# Create your models here.


class CurrencyModel(models.Model):
    prefix = models.CharField(max_length=10,blank=True,null=True)
    short_key = models.CharField(max_length=100,unique=True)
    rate = models.DecimalField(max_digits=8,decimal_places=5,default=0)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.short_key
    
    
class PaymentGatewayModel(models.Model):
    name = models.CharField(max_length=255,unique=True)
    currency = models.ForeignKey(CurrencyModel,on_delete=models.CASCADE)
    api_key = models.CharField(max_length=255)
    access_key = models.CharField(max_length=255)
    test_api_key = models.CharField(max_length=255)
    test_access_key = models.CharField(max_length=255)
    test_mode = models.BooleanField(default=True)
    payment_gateway_class = models.CharField(max_length=500)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    

status_choices = (
    ('processing','Processing'),
    ('success','Success'),
    ('cancelled','Cancelled'),
    ('failed','Failed')
)

class OrderModel(models.Model):
    description = models.TextField()
    amount = models.DecimalField(max_digits=10,decimal_places=3)
    currency = models.CharField(max_length=10)
    customer_name = models.CharField(max_length=255)
    customer_email = models.CharField(max_length=255)
    customer_phone = models.CharField(max_length=255)
    status = models.CharField(max_length=50,choices=status_choices,default='Processing')