from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.generics import CreateAPIView, UpdateAPIView
from .models import Address
from .serializers import AddressSerializer


class AddressView(CreateAPIView, UpdateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = AddressSerializer
    queryset = Address.objects.all()

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        obj = queryset.get(user=self.request.user)
        self.check_object_permissions(self.request, obj)
        return obj

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    # def perform_update(self, serializer):
    #     import ipdb
    #     ipdb.set_trace()
    #     address = Address.objects.filter(user=self.request.user)
    #     serializer.save(address, user=self.request.user)
