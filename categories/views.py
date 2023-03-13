from .models import Category
from rest_framework import generics
from .serializers import CategorySerializer
from .permissions import IsAdmPermissions


class CategoryView(generics.ListCreateAPIView):
    permission_classes = [IsAdmPermissions]

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
