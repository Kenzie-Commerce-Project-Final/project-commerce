from rest_framework import serializers
from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    def create(self, validated_data: dict) -> Product:

        data = validated_data.copy()

        if data["stock"] == 0:
            data["is_available"] = False

        return Product.objects.create(**data)

    def update(self, instance: Product, validated_data: dict) -> Product:
        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.save()

        return instance

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "stock",
            "is_available",
            "price",
            "category",
            "user",
        ]


class ProductCartSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    name = serializers.CharField()
    price = serializers.DecimalField()
    amount = serializers.IntegerField()
