# serializers.py

from rest_framework import serializers
from rest_enumfield import EnumField
from .models import QueueEntryStatus


class HumanSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    status = EnumField(QueueEntryStatus, required=False)
class QueueEntrySerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    user_ids = HumanSerializer(many=True, required=False)
    created_at = serializers.DateTimeField(read_only=True)
    notified_at = serializers.DateTimeField(read_only=True, allow_null=True)
    served_at = serializers.DateTimeField(read_only=True, allow_null=True)

class IDSerializer(serializers.Serializer):
    id = serializers.IntegerField()

class AddUserSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    user_id = serializers.IntegerField()

class OperationSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    done = serializers.BooleanField(read_only=True)
    result = serializers.DictField(read_only=True, allow_null=True)

