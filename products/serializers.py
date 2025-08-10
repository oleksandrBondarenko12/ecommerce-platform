# In products/serializers.py

from rest_framework import serializers
from .models import Product, Category


# This serializer is for creating/updating products.
# It accepts a simple ID for the category.
class ProductWriteSerializer(serializers.ModelSerializer):
    # This field expects the primary key (ID) of a Category.
    # It will automatically look up the Category object.
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())

    class Meta:
        model = Product
        # We only need the fields that a user provides when creating/updating.
        fields = ['name', 'description', 'price', 'category', 'image', 'in_stock']


# This is your existing serializer, now used only for reading data.
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


# This serializer is for reading/listing products (GET requests).
# It displays the full nested category object.
class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)  # `read_only=True` is a good practice here

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'category', 'image',
                  'in_stock', 'created_at']
