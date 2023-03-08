from .models import Product
from .serializers import ProductSerializer
from rest_framework import generics
from rest_framework.permissions import IsAdminUser
from categories.models import Category
from .permissions import MyCustomPermissions


class ProductView(generics.ListCreateAPIView):
    # permission_classes = [MyCustomPermissions]

    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)


class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminUser]

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
