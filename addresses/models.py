from django.db import models
import uuid


class Address(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    city = models.CharField(max_length=127)
    zip_code = models.CharField(max_length=8)
    street = models.CharField(max_length=127)
    district = models.CharField(max_length=127)
    number = models.IntegerField()
    complement = models.TextField(max_length=300)
    user = models.OneToOneField(
        "users.User",
        on_delete=models.CASCADE,
        related_name="address",
    )
