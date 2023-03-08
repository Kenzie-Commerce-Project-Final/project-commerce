from rest_framework import permissions
from .models import Product
from rest_framework.views import View, Request


class MyCustomPermissions(permissions.BasePermission):
    def has_permission(self, request: Request):
        return request.user.is_authenticated and request.user.is_staff
