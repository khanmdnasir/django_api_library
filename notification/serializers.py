from rest_framework import serializers
from .models import *

class SMSConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = SMSConfigModel
        fields = '__all__'
        
class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationModel
        fields = '__all__'

class SMSScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = SMSScheduleModel
        fields = '__all__'

class EmailScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailScheduleModel
        fields = '__all__'
