from django.db import models
import uuid


class Status(models.TextChoices):
    PENDING = "PENDENTE"
    REQUEST_MADE = ("PEDIDO REALIZADO",)
    IN_PROGRESS = ("EM ANDAMENTO",)
    DONE = "CONCLUÍDO"


class Cart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    items_count = models.IntegerField(default=0)
    total_price = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    status = models.CharField(
        max_length=50, choices=Status.choices, default=Status.PENDING
    )
    crated_at = models.DateTimeField(auto_now_add=True)
    products = models.ManyToManyField("products.Product", through="carts.CartProduct")
    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="carts",
    )


class CartProduct(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey("products.Product", on_delete=models.CASCADE)
    cart = models.ForeignKey("carts.Cart", on_delete=models.CASCADE)
    amount = models.IntegerField()
