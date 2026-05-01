from rest_framework.permissions import BasePermission


class IsAuthenticatedActiveUser(BasePermission):
    message = "Active authenticated user is required."

    def has_permission(self, request, view):
        user = request.user
        return bool(user and user.is_authenticated and user.is_active)
