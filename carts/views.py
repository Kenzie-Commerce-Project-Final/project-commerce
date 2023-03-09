from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    UpdateAPIView,
    DestroyAPIView,
)
from rest_framework.permissions import IsAuthenticated
from carts.models import Cart, Status
from carts.serializers import CartSerializer, CartProductSerializer


class CartView(ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Cart.objects.all()

        return Cart.objects.filter(user=self.request.user, status=Status.REQUEST_MADE)


class CartViewProduct(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CartProductSerializer

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)


class CartViewProductById(UpdateAPIView, DestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CartSerializer
