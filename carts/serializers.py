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
        read_only_fields = ["id", "created_at"]
        extra_kwargs = {"items_count": {"min_value": 0}}

    def create(self, validated_data: dict) -> Cart:
        return validated_data.save()
