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


class IsPermissionPatchDelete(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser or request.user.is_staff and obj == request.user:
            return True
