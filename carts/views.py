from rest_framework.generics import ListCreateAPIView
from carts.models import Cart
from carts.serializers import CartSerializer
from users.models import User


class CartView(ListCreateAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

    def perform_create(self, serializer):

        # import ipdb

        user = User.objects.first()
        # ipdb.set_trace()

        return serializer.save(user=user)
