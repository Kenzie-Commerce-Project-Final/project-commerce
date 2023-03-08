from rest_framework import serializers, validators
from carts.models import Cart, Status
from products.models import Product
from django.shortcuts import get_object_or_404
from django.db.models import Sum


class CartSerializer(serializers.ModelSerializer):
    items_count = serializers.SerializerMethodField()
    total_price = serializers.SerializerMethodField()

    def get_items_count(self, obj):
        return obj.products.all().count()

    def get_total_price(self, obj):
        return obj.products.all().aggregate(Sum("price")).get("price__sum")

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
        read_only_fields = ["id", "total_price", "created_at", "products", "user_id"]
        extra_kwargs = {"items_count": {"min_value": 0}}

    def create(self, validated_data: dict) -> Cart:
        user = validated_data.get("user")
        find_cart = Cart.objects.filter(status=Status.REQUEST_MADE, user=user).first()

        if find_cart and find_cart.status == Status.REQUEST_MADE:
            raise validators.ValidationError("There is an open cart.")

        return Cart.objects.create(**validated_data)


class CartProductSerializer(serializers.Serializer):
    product_id = serializers.UUIDField(write_only=True)
    message = serializers.SerializerMethodField(read_only=True)

    def get_message(self, obj):
        return "Product added"

    def create(self, validated_data):
        user = validated_data.get("user")
        product = get_object_or_404(Product, id=validated_data.get("product_id"))

        cart = Cart.objects.filter(user=user, status=Status.REQUEST_MADE).first()

        cart.products.add(product)

        cart.save()

        return cart
