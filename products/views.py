from .models import Product
from .serializers import ProductSerializer
from rest_framework import generics
from rest_framework_simplejwt.authentication import JWTAuthentication


class ProductView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
