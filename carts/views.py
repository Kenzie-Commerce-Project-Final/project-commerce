from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    UpdateAPIView,
    DestroyAPIView,
)
from rest_framework.views import APIView, Response, status
from rest_framework.permissions import IsAuthenticated
from carts.models import Cart, CartProduct, Status
from carts.serializers import CartSerializer, CartProductSerializer
from utils.cart.count_items import count_items
from utils.cart.sum_total_price import sum_total_price
from rest_framework.validators import ValidationError
from carts.permissions import IsSeller


class CartView(ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

    def get_queryset(self):
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
        cart = queryset.get(
            user=self.request.user, products=product_id, status=Status.PENDING
        )
        carts_products = CartProduct.objects.get(cart=cart, product=product_id)
        self.check_object_permissions(self.request, carts_products)
        return carts_products

    def perform_destroy(self, instance):
        products_cart = instance.cart.products.all()

        if len(products_cart) == 1:
            return instance.cart.delete()

        instance.delete()

        cart = instance.cart

        cart.items_count = count_items(cart)
        cart.total_price = sum_total_price(cart)
        cart.save()


class CartViewCheckout(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        carts = Cart.objects.filter(user=user, status=Status.PENDING)

        if not carts:
            return Response(
                {"message": "User does not have open carts."},
                status.HTTP_400_BAD_REQUEST,
            )

        for cart in carts:
            carts_products = CartProduct.objects.filter(cart=cart)
            for cart_product in carts_products:
                if not cart_product.product.is_available:
                    raise ValidationError("Product is not available.")

                if cart_product.product.stock <= cart_product.amount:
                    raise ValidationError(
                        f"Product quantity exceeded inventory, inventory available {cart_product.product.stock}."
                    )

                cart_product.product.stock = (
                    cart_product.product.stock - cart_product.amount
                )
                cart_product.product.save()

            cart.status = Status.REQUEST_MADE
            cart.save()
        return Response({"message": "Order placed."}, status.HTTP_201_CREATED)


class CartOrderView(ListAPIView):
    permission_classes = [IsAuthenticated, IsSeller]
    serializer_class = CartSerializer

    def get_queryset(self):
        return Cart.objects.filter(
            products__user_id=self.request.user, status=Status.REQUEST_MADE
        )


class CartOrderViewId(UpdateAPIView):
    permission_classes = [IsAuthenticated, IsSeller]
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
