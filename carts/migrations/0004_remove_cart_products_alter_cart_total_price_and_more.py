# Generated by Django 4.1.7 on 2023-03-08 22:40

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):
    dependencies = [
        ("products", "0003_rename_is_avaliable_product_is_available"),
        ("carts", "0003_cart_products"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="cart",
            name="products",
        ),
        migrations.AlterField(
            model_name="cart",
            name="total_price",
            field=models.DecimalField(decimal_places=2, default=0, max_digits=8),
        ),
        migrations.CreateModel(
            name="CartProduct",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("amount", models.IntegerField()),
                (
                    "cart",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="cart_products",
                        to="carts.cart",
                    ),
                ),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="product_carts",
                        to="products.product",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="cart",
            name="cart_product",
            field=models.ManyToManyField(
                related_name="products_cart",
                through="carts.CartProduct",
                to="products.product",
            ),
        ),
    ]
