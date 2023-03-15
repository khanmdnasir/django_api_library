from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.serializers import Serializer
from .models import *

User = get_user_model()


class UserSerializer(Serializer):
    class Meta:
        model = User
        fields = '__all__'


class IssueTypesSerializer(serializers.ModelSerializer):

    class Meta:
        model = IssueTypesModel
        fields = '__all__'

class TicketSerializer(serializers.ModelSerializer):

    support_agent = UserSerializer(many=False, read_only=True)
    approved_by = UserSerializer(many=False, read_only=True)
    class Meta:
        model = TicketModel
        fields = ('id', 'unique_id', 'title', 'issue_type', 'phone', 'email', 'is_active', 'description', 'is_open', 'status', 'is_registered_user', 'support_agent', 'support_agent_id', 'priority', 'due_date', 'approved_by', 'approved_by_id')

        extra_kwargs = {
            'support_agent_id': {'source': 'support_agent', 'write_only': True},
            'approved_by_id': {'source': 'approved_by', 'write_only': True}
        }


class TicketCommentsSerializer(serializers.ModelSerializer):
    author = UserSerializer(many=False, read_only=True)
    class Meta:
        model = TicketCommentsModel
        fields = ('id', 'unique_id', 'comment', 'is_customer', 'author', 'author_id', 'is_active', 'created_at', 'updated_at', 'updated_by')

        extra_kwargs = {
            'author_id': {'source': 'author', 'write_only': True}
        }

class TicketLogsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketLogsModel
        fields = '__all__'