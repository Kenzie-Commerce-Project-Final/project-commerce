from rest_framework import permissions
from rest_framework.views import Request, View
from .models import User


class IsAdmOrUserCommon(permissions.BasePermission):
    def has_object_permission(self, request: Request, view: View, user: User):
        if request.user.is_superuser and request.user.is_authenticated:
            return True
        import ipdb

        # ipdb.set_trace()
        return request.user.is_authenticated and request.user.id == user.id
