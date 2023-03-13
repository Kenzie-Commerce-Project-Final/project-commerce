from rest_framework import serializers
from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    def create(self, validated_data: dict) -> Product:

        data = validated_data.copy()

        if data["stock"] == 0:
            data["is_available"] = False

        return Product.objects.create(**data)

    def update(self, instance: Product, validated_data: dict) -> Product:
        stock = validated_data.get("stock", None)

        if stock == 0:
            validated_data.update({"is_available": False})
        elif stock != 0:
            validated_data.update({"is_available": True})

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


class ProductOnCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "price",
            "is_available",
            "category",
            "user",
        ]
