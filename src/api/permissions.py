from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    """Allow superuser access only if the user is an admin."""

    def has_permission(self, request, view):
        return request.user.is_superuser
