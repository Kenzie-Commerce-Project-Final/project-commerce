from rest_framework.permissions import BasePermission
from rest_framework.views import Request, View


class IsSeller(BasePermission):
    def has_permission(self, request: Request, view: View):
        return request.user and request.user.is_staff
