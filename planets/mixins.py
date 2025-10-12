from django.conf import settings
from rest_framework.permissions import IsAuthenticated, AllowAny


class OptionalAuthMixin:
    """
    Mixin to set permissions dynamically based on settings only for testing purposes.
    """
    def get_permissions(self):
        if getattr(settings, 'PLANETS_AUTH_REQUIRED', False):
            permission_classes = [IsAuthenticated]
            print("Authentication is required for this view.")
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]