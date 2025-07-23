# In products/views.py

from rest_framework import permissions
from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    CreateAPIView,
    UpdateAPIView,
    DestroyAPIView,
)
from .models import Product
# Import both serializers
from .serializers import ProductSerializer, ProductWriteSerializer


# Anyone can GET. This uses the READ serializer.
class ProductListView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer # For displaying products


class ProductDetailView(RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer # For displaying a single product

# Only admins can POST. This uses the WRITE serializer.
class ProductCreateView(CreateAPIView):
    queryset = Product.objects.all()
    # Use the write serializer for creating
    serializer_class = ProductWriteSerializer
    permission_classes = [permissions.IsAdminUser]

# Only admins can PUT/PATCH. This also uses the WRITE serializer.
class ProductUpdateView(UpdateAPIView):
    queryset = Product.objects.all()
    # Use the write serializer for updating
    serializer_class = ProductWriteSerializer
    permission_classes = [permissions.IsAdminUser]

# Only admins can delete. This doesn't heavily rely on the serializer for input
class ProductDeleteView(DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer # Can be any of them, it just needs to identify the object.
    permission_classes = [permissions.IsAdminUser]
