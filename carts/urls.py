from django.urls import path
from carts.views import CartView

urlpatterns = [
    path("carts/", CartView.as_view()),
]
