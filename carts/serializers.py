from rest_framework import serializers, validators
from carts.models import Cart, Status


class CartSerializer(serializers.ModelSerializer):
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
