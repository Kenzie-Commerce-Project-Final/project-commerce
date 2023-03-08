from .models import Category
from rest_framework import generics
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import CategorySerializer
from .permissions import IsAdmPermissions


class CategoryView(generics.ListCreateAPIView):
    # permission_classes = [IsAdmPermissions]

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
