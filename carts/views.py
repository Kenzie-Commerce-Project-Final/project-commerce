from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    UpdateAPIView,
    DestroyAPIView,
)
from rest_framework.permissions import IsAuthenticated
from carts.models import Cart, CartProduct, Status
from carts.serializers import CartSerializer, CartProductSerializer


class CartView(ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Cart.objects.all()

        return Cart.objects.filter(user=self.request.user, status=Status.PENDING)


class CartViewProduct(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CartProductSerializer

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)


class CartViewProductById(UpdateAPIView, DestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CartProductSerializer
    queryset = Cart.objects.all()
    lookup_url_kwarg = "product_id"

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        product_id = self.kwargs.get("product_id")
        cart = queryset.get(user=self.request.user, carts_products=product_id)
        carts_products = CartProduct.objects.get(cart=cart, product=product_id)
        self.check_object_permissions(self.request, carts_products)
        return carts_products

    def perform_destroy(self, instance):

        return
