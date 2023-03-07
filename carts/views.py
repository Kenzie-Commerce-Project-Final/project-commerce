from rest_framework.generics import ListAPIView
from carts.models import Cart


class CartView(ListAPIView):
    queryset = Cart.objects.all()
