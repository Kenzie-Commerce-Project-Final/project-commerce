from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import Response
from .models import User
from .serializers import UserSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from .permissions import IsAdmOrUserCommon
from products.models import Product
from products.serializers import ProductSerializer

# Create your views here.


class UserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdmOrUserCommon]

    queryset = User.objects.all()
    serializer_class = UserSerializer


class SellerProductsView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]

    queryset = Product.objects.none()
    http_method_names = ["get"]

    def list(self, request, pk):
        products = Product.objects.filter(user_id=pk)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
