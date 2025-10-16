from django.conf import settings
from rest_framework.permissions import IsAuthenticated, AllowAny


class OptionalAuthMixin:
    """
    Mixin to set permissions dynamically based on settings only for testing purposes.
    """
    def get_permissions(self):
        auth_required = getattr(settings, 'API_AUTH_REQUIRED', False)
        if auth_required:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]
