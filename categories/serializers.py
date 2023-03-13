from rest_framework import serializers
from .models import Category


class CategorySerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        return Category.objects.create(**validated_data)

    class Meta:
        model = Category
        fields = [
            "id",
            "name",
        ]
