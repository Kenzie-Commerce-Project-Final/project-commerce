from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import User
from django.contrib.auth.hashers import make_password


class UserSerializer(serializers.ModelSerializer):
    def create(self, validated_data: dict) -> User:
        return User.objects.create_user(**validated_data)

    def update(self, instance: User, validated_data: dict) -> User:
        for key, value in validated_data.items():
            if key == "password":
                instance.set_password(value)
            setattr(instance, key, value)
        instance.password = make_password(instance.password)
        instance.save()

        return instance

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "password",
            "phone_number",
            "cpf",
            "is_superuser",
            "is_staff",
        ]
        extra_kwargs = {
            "username": {
                "validators": [
                    UniqueValidator(
                        queryset=User.objects.all(),
                        message="A user with that username already exists.",
                    )
                ],
            },
            "email": {
                "validators": [
                    UniqueValidator(
                        queryset=User.objects.all(),
                        message="This field must be unique.",
                    )
                ]
            },
            "password": {"write_only": True},
            "is_superuser": {"read_only": True},
            "phone_number": {"max_length": 11, "min_length": 11},
            "cpf": {"max_length": 11, "min_length": 11},
        }
