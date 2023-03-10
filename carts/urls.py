from django.urls import path
from carts.views import CartView, CartViewProduct, CartViewProductById, CartViewCheckout

urlpatterns = [
    path("", CartView.as_view()),
    path("products/", CartViewProduct.as_view()),
    path("products/<uuid:product_id>/", CartViewProductById.as_view()),
    path("checkout/", CartViewCheckout.as_view()),
]
