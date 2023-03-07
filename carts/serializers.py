from rest_framework import serializers
from carts.models import Cart, Status


class CartSerializer(serializers.ModelField):
    status = serializers.ChoiceField(
        choices=Status.choices, default=Status.REQUEST_MADE
    )

    class Meta:
        model = Cart
        fields = [
            "id",
            "items_count",
            "total_price",
            "status",
            "crated_at",
            "products",
            "user",
        ]
        extra_kwargs = {"items_count": {"min_value": 0}}
