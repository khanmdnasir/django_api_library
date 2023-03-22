from rest_framework import serializers
from .models import *

class DBBackupSerializer(serializers.ModelSerializer):
    class Meta:
        model = DbBackupModel
        fields = '__all__'