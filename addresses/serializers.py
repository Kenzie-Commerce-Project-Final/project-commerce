from rest_framework import serializers
from .models import Address


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ["id", "city", "zip_code", "street", "number", "complement", "user"]
