from django.db import models
import uuid


class Status(models.TextChoices):
    REQUEST_MADE = ("PEDIDO REALIZADO",)
    IN_PROGRESS = ("EM ANDAMENTO",)
    DONE = "CONCLUÍDO"


class Cart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    items_count = models.IntegerField(default=0)
    total_price = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    status = models.CharField(
        max_length=50, choices=Status.choices, default=Status.REQUEST_MADE
    )
    crated_at = models.DateTimeField(auto_now_add=True)
    products = models.ManyToManyField("products.Product", related_name="cart_products")
    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="carts",
    )
