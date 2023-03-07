from .models import Product
from .serializers import ProductSerializer
from rest_framework import generics
from rest_framework_simplejwt.authentication import JWTAuthentication
from .permissions import MyCustomPermissions


class ProductView(generics.CreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [MyCustomPermissions]

    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [MyCustomPermissions]

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
