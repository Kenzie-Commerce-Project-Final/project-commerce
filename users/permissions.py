from rest_framework import permissions
from rest_framework.views import Request, View
from .models import User


class IsAdmOrUserCommon(permissions.BasePermission):
    def has_object_permission(self, request: Request, view: View, user: User):
        if request.user.is_superuser and request.user.is_authenticated:
            return True
        return request.user.is_authenticated and request.user.id == user.id


class IsAdmToReadUsers(permissions.BasePermission):
    def has_permission(self, request, view) -> bool:
        if request.method in permissions.SAFE_METHODS:
            if not request.user.is_superuser:
                return False
        return True
