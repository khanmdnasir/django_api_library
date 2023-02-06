from rest_framework import serializers
from .models import *

class ActionTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActionType
        fields = '__all__'

class AuthenticationLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthenticationLog
        fields = '__all__'

class ActivityLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityLog
        fields = '__all__'