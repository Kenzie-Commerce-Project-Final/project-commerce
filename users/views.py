from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import Response
from .models import User
from .serializers import UserSerializer
from .permissions import IsAdmOrUserCommon, IsAdmToReadUsers
from products.models import Product
from products.serializers import ProductSerializer
from carts.models import Cart, Status
from carts.serializers import CartSerializer
from django.shortcuts import get_object_or_404

# Create your views here.


class UserView(generics.ListCreateAPIView):
    permission_classes = [IsAdmToReadUsers]

    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdmOrUserCommon]

    queryset = User.objects.all()
    serializer_class = UserSerializer


class SellerProductsView(generics.ListAPIView):
    queryset = Product.objects.none()
    http_method_names = ["get"]

    def list(self, request, pk):
        products = Product.objects.filter(user_id=pk)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)


class PurchaseHistoryView(generics.ListAPIView):
    permission_classes = [IsAdmOrUserCommon]
    serializer_class = CartSerializer

    def get_queryset(self):
        user = get_object_or_404(User, id=self.kwargs["pk"])
        self.check_object_permissions(self.request, user)

        return Cart.objects.filter(
            user_id=self.kwargs["pk"],
            status__in=[Status.DONE, Status.IN_PROGRESS, Status.REQUEST_MADE],
        )
