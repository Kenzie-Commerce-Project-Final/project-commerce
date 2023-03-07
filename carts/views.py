from rest_framework.generics import ListCreateAPIView
from carts.models import Cart
from carts.serializers import CartSerializer


class CartView(ListCreateAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
