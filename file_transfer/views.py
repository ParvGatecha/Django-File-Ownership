from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.db import transaction
from rest_framework import generics, views, status
from rest_framework.response import Response
from .models import File, TransferHistory
from .serializers import FileSerializer, TransferHistorySerializer

# 1. View for creating (uploading) and listing files
class FileListCreateView(generics.ListCreateAPIView):
    serializer_class = FileSerializer

    def get_queryset(self):
        # Users can only see files they currently own
        return File.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        # When a file is created, the owner and original_owner are the same
        serializer.save(
            owner=self.request.user, 
            original_owner=self.request.user
        )

# 2. View for the Transfer logic
class TransferAPIView(views.APIView):
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        file_id = request.data.get('file_id')
        to_user_id = request.data.get('to_user_id')

        # --- Validation ---
        if not file_id or not to_user_id:
            return Response({"error": "file_id and to_user_id are required."}, status=status.HTTP_400_BAD_REQUEST)
        
        file = get_object_or_404(File, id=file_id)
        to_user = get_object_or_404(User, id=to_user_id)
        from_user = request.user

        # Check if the requester is the current owner
        if file.owner != from_user:
            return Response({"error": "Permission denied. You are not the current owner of this file."}, status=status.HTTP_403_FORBIDDEN)
        
        if file.owner == to_user:
            return Response({"error": "Cannot transfer file to the current owner."}, status=status.HTTP_400_BAD_REQUEST)

        # --- Logic ---
        # 1. Update file ownership
        file.owner = to_user
        file.save()

        # 2. Create transfer history record
        TransferHistory.objects.create(
            file=file,
            from_user=from_user,
            to_user=to_user,
            action='TRANSFER'
        )

        return Response({"success": f"File '{file.name}' transferred to {to_user.username}."}, status=status.HTTP_200_OK)

# 3. View for the Revoke logic
class RevokeAPIView(views.APIView):
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        file_id = request.data.get('file_id')

        # --- Validation ---
        if not file_id:
            return Response({"error": "file_id is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        file = get_object_or_404(File, id=file_id)
        original_owner = request.user

        # Check if the requester is the original owner
        if file.original_owner != original_owner:
            return Response({"error": "Permission denied. You are not the original owner of this file."}, status=status.HTTP_403_FORBIDDEN)
        
        if file.owner == original_owner:
             return Response({"error": "Cannot revoke. You are already the current owner."}, status=status.HTTP_400_BAD_REQUEST)

        # --- Logic ---
        current_owner = file.owner
        
        # 1. Update file ownership back to original owner
        file.owner = original_owner
        file.save()

        # 2. Create history record for the revoke action
        TransferHistory.objects.create(
            file=file,
            from_user=current_owner, # The user who lost ownership
            to_user=original_owner,   # The user who regained ownership
            action='REVOKE'
        )

        return Response({"success": f"Ownership of '{file.name}' has been revoked and returned to you."}, status=status.HTTP_200_OK)

# 4. View to see a specific file's history
class FileHistoryView(generics.ListAPIView):
    serializer_class = TransferHistorySerializer

    def get_queryset(self):
        file_id = self.kwargs['file_id']
        file = get_object_or_404(File, id=file_id)

        # You can only see the history if you are the original owner or current owner
        if self.request.user == file.original_owner or self.request.user == file.owner:
            return TransferHistory.objects.filter(file_id=file_id).order_by('-timestamp')
        
        # Return an empty queryset if user is not authorized to see the history
        return TransferHistory.objects.none()