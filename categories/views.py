from .models import Category
from rest_framework import generics
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import CategorySerializer


class CategoryView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
