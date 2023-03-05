from rest_framework import serializers
from .models import *

class StripeconfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = StripeConfig
        fields = '__all__'

class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = CurrencyModel
        fields = '__all__'

class PaymentGatewaySerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentGatewayModel
        fields = '__all__'