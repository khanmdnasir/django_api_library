from rest_framework import serializers
from .models import *

class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentModel
        fields = '__all__'

class AppSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppSettings
        fields = '__all__'