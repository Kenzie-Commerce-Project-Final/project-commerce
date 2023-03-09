from rest_framework import serializers, validators
from carts.models import Cart, CartProduct, Status
from products.models import Product
from django.shortcuts import get_object_or_404


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = [
            "id",
            "items_count",
            "total_price",
            "status",
            "crated_at",
            "carts_products",
            "user_id",
        ]
        read_only_fields = ["id", "created_at", "user_id"]
        depth = 1

    def create(self, validated_data: dict) -> Cart:
        return Cart.objects.create(**validated_data)


class CartProductSerializer(serializers.ModelSerializer):
    product_id = serializers.UUIDField()
    message = serializers.SerializerMethodField(read_only=True)

    def get_message(self, obj):
        return "Product added"

    class Meta:
        model = CartProduct
        fields = ["id", "product_id", "amount", "message"]
        extra_kwargs = {"amount": {"min_value": 1}}

    def create(self, validated_data):
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
            cart
            for cart in carts_pending
            if cart.carts_products.first().user == product.user
        ]

        if not cart:
            cart = Cart.objects.create(user=user)
            cart_products = CartProduct.objects.create(
                cart=cart, product=product, amount=amount
            )
            return cart_products

        find_cart_product = CartProduct.objects.filter(
            cart=cart[0], product=product
        ).first()

        if find_cart_product:
            find_cart_product.amount = amount
            find_cart_product.save()
            return find_cart_product

        cart_products = CartProduct.objects.create(
            cart=cart[0], product=product, amount=amount
        )
        return cart_products
