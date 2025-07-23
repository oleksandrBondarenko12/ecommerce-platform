# In products/serializers.py (Recommended version)

from rest_framework import serializers
from .models import Product, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class ProductSerializer(serializers.ModelSerializer):
    # This nests the category details, which is great for read operations.
    category = CategorySerializer() 

    class Meta:
        model = Product
        # Explicitly list fields. Note the typo fix from 'create_at' to 'created_at'.
        fields = ['id', 'name', 'description', 'price', 'category', 'image', 
                  'in_stock', 'created_at']
