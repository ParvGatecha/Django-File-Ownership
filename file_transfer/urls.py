# Create this new file

from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import (
    FileListCreateView, 
    TransferAPIView, 
    RevokeAPIView,
    FileHistoryView
)

urlpatterns = [
    # Auth
    path('get-token/', obtain_auth_token, name='get-token'),

    # Core Functionality
    path('files/', FileListCreateView.as_view(), name='file-list-create'),
    path('transfer/', TransferAPIView.as_view(), name='transfer-file'),
    path('revoke/', RevokeAPIView.as_view(), name='revoke-transfer'),

    # History
    path('files/<int:file_id>/history/', FileHistoryView.as_view(), name='file-history'),
]