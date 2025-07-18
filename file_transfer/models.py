from django.db import models
from django.contrib.auth.models import User

# File Model
class File(models.Model):
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to='uploads/')
    # The original_owner never changes. It's the user who uploaded the file.
    original_owner = models.ForeignKey(User, related_name='original_files', on_delete=models.CASCADE)
    # The owner is the current owner of the file. This will change on transfer.
    owner = models.ForeignKey(User, related_name='owned_files', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} (Owned by: {self.owner.username})"

# TransferHistory Model
class TransferHistory(models.Model):
    ACTION_CHOICES = (
        ('TRANSFER', 'Transfer'),
        ('REVOKE', 'Revoke'),
    )
    
    file = models.ForeignKey(File, related_name='transfer_history', on_delete=models.CASCADE)
    from_user = models.ForeignKey(User, related_name='transfers_made', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='transfers_received', on_delete=models.CASCADE)
    action = models.CharField(max_length=10, choices=ACTION_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.file.name} - {self.action} from {self.from_user.username} to {self.to_user.username}"