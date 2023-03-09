from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.generics import CreateAPIView
from .models import Address
from .serializers import AddressSerializer


class AddressView(CreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Address.objects.all()
    serializer_class = AddressSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
