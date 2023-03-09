from django.urls import path
from carts.views import CartView, CartViewProduct

urlpatterns = [
    path("", CartView.as_view()),
    path("products/", CartViewProduct.as_view()),
]
