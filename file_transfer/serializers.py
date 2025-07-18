from rest_framework import serializers
from django.contrib.auth.models import User
from .models import File, TransferHistory

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

class FileSerializer(serializers.ModelSerializer):
    # Use read-only fields to display user info without making them writable
    owner = serializers.ReadOnlyField(source='owner.username')
    original_owner = serializers.ReadOnlyField(source='original_owner.username')

    class Meta:
        model = File
        fields = ['id', 'name', 'file', 'owner', 'original_owner', 'created_at']
        read_only_fields = ['owner', 'original_owner', 'created_at']

class TransferHistorySerializer(serializers.ModelSerializer):
    file = serializers.StringRelatedField()
    from_user = serializers.StringRelatedField()
    to_user = serializers.StringRelatedField()

    class Meta:
        model = TransferHistory
        fields = ['id', 'file', 'from_user', 'to_user', 'action', 'timestamp']