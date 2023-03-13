from .models import Product
from .serializers import ProductSerializer
from rest_framework import generics
from .permissions import MyCustomPermissions, IsOwnerOrSuperUser
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status


class ProductView(generics.ListCreateAPIView):
    permission_classes = [MyCustomPermissions]
    serializer_class = ProductSerializer

    def get_queryset(self):
        route_parameter_name = self.request.query_params.get("name")
        route_parameter_category = self.request.query_params.get("category_id")

        if route_parameter_name:
            queryset_params = Product.objects.filter(
                name__icontains=route_parameter_name
            )
            return queryset_params

        if route_parameter_category:
            queryset_params = Product.objects.filter(category=route_parameter_category)
            return queryset_params

        return Product.objects.all()

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)


class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsOwnerOrSuperUser]

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_url_kwarg = "id"

    def perform_destroy(self, instance):
        product = get_object_or_404(Product, id=instance.id)
        self.check_object_permissions(self.request, product)

        if product:
            instance.is_available = False
            instance.save()

        return Response(status=status.HTTP_204_NO_CONTENT)
