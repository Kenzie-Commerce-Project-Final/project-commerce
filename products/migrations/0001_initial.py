# Generated by Django 4.1.7 on 2023-03-07 14:48

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("categories", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Product",
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
                ("name", models.CharField(max_length=120)),
                ("stock", models.IntegerField()),
                ("is_avaliable", models.BooleanField(default=True)),
                ("price", models.DecimalField(decimal_places=2, max_digits=8)),
                (
                    "category",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="products",
                        to="categories.category",
                    ),
                ),
            ],
        ),
    ]
