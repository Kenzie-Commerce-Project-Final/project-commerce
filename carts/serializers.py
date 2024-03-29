from rest_framework import serializers, validators
from carts.models import Cart, CartProduct, Status
from products.models import Product
from django.shortcuts import get_object_or_404
from utils.cart.count_items import count_items
from utils.cart.sum_total_price import sum_total_price
from products.serializers import ProductOnCartSerializer
from django.core.mail import send_mail
from django.conf import settings


class CartSerializer(serializers.ModelSerializer):
    products = ProductOnCartSerializer(many=True)

    class Meta:
        model = Cart
        fields = [
            "id",
            "items_count",
            "total_price",
            "status",
            "crated_at",
            "products",
            "user_id",
        ]
        read_only_fields = [
            "id",
            "created_at",
            "user_id",
        ]
        extra_kwargs = {
            "status": {
                "error_messages": {
                    "invalid_choice": f"status needs to be '{Status.IN_PROGRESS}' or '{Status.DONE}'"
                },
            }
        }

    def create(self, validated_data: dict) -> Cart:
        return Cart.objects.create(**validated_data)

    def update(self, instance: Cart, validated_data: dict) -> Cart:
        status = validated_data.get("status", None)
        if not status:
            raise validators.ValidationError({"status": "is required field."})
        setattr(instance, "status", status)
        instance.save()
        send_mail(
            subject='Status do pedido alterado',
            message=f'O seu pedido realizado da empresa {instance.products.first().user.first_name} foi alterado para {instance.status}.',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[instance.user.email],
            fail_silently=False
        )
        return instance


class CartProductSerializer(serializers.ModelSerializer):
    product_id = serializers.UUIDField()

    class Meta:
        model = CartProduct
        fields = ["id", "product_id", "amount"]
        extra_kwargs = {"amount": {"min_value": 1}}

    def create(self, validated_data: dict) -> CartProduct:
        user = validated_data.get("user")
        amount = validated_data.get("amount")
        product_id = validated_data.get("product_id")

        product = get_object_or_404(Product, id=product_id)

        if not product.is_available:
            raise validators.ValidationError("Product is not available.")

        if product.stock < amount:
            raise validators.ValidationError(
                f"Product quantity exceeded inventory, inventory available {product.stock}."
            )

        carts_pending = Cart.objects.filter(user=user, status=Status.PENDING)

        cart = [
            cart for cart in carts_pending if cart.products.first().user == product.user
        ]

        if not cart:
            cart = Cart.objects.create(user=user)
            cart_products = CartProduct.objects.create(
                cart=cart, product=product, amount=amount
            )
            cart.items_count = count_items(cart)
            cart.total_price = sum_total_price(cart)
            cart.save()
            return cart_products

        cart = cart[0]

        find_cart_product = CartProduct.objects.filter(
            cart=cart, product=product
        ).first()

        if find_cart_product:
            raise validators.ValidationError("Product has already been added to cart.")

        cart_products = CartProduct.objects.create(
            cart=cart, product=product, amount=amount
        )
        cart.items_count = count_items(cart)
        cart.total_price = sum_total_price(cart)
        cart.save()
        return cart_products

    def update(self, instance: CartProduct, validated_data: dict) -> CartProduct:
        amount = validated_data.get("amount", None)

        if not amount:
            raise validators.ValidationError({"amount": "This field is required."})

        setattr(instance, "amount", amount)
        instance.save()

        cart = instance.cart

        cart.items_count = count_items(cart)
        cart.total_price = sum_total_price(cart)
        cart.save()

        return instance
