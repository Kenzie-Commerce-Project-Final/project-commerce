from rest_framework import permissions
from rest_framework.views import View, Request


class MyCustomPermissions(permissions.BasePermission):
    def has_permission(self, request: Request, view: View):
        return bool(
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
            and request.user.is_staff
            or request.user.is_superuser
        )


class IsOwnerOrSuperUser(permissions.BasePermission):
    def has_object_permission(self, request: Request, view: View, obj):
        if (
            request.method in permissions.SAFE_METHODS
            or request.user.is_superuser
            and request.user.is_authenticated
        ):
            return True
        return request.user.is_authenticated and request.user.id == obj.user.id
