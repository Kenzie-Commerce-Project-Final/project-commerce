from .models import Product
from .serializers import ProductSerializer
from rest_framework import generics
from .permissions import MyCustomPermissions, IsPermissionPatchDelete


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


class ProductDetailView(generics.RetrieveAPIView):
    permission_classes = [MyCustomPermissions]

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_url_kwarg = "id"


class ProductDetailUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    # permission_classes = [MyCustomPermissions]

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_url_kwarg = "deletePatch_id"
