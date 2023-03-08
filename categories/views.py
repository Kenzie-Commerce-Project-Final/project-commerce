from .models import Category
from rest_framework import generics
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import CategorySerializer
from rest_framework.permissions import IsAdminUser


class CategoryView(generics.ListCreateAPIView):
    permission_classes = [IsAdminUser]

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
