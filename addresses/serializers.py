from rest_framework import serializers
from .models import Address


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ["id", "city", "zip_code", "street", "district", "number", "complement", "user_id"]

    zip_code = serializers.CharField(max_length=8, min_length=8)

    def create(self, validated_data: dict) -> Address:
        return Address.objects.create(**validated_data)
