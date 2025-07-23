from rest_framework import serializers
from .models import Product  # Make sure Product model exists

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'  # or specify fields manually

