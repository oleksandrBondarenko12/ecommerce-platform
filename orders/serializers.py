# In orders/serializers.py
from rest_framework import serializers
from .models import Order, OrderItem
from cart.serializers import SimpleProductSerializer


class OrderItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity', 'price_at_purchase']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    user = serializers.StringRelatedField()  # Display username

    class Meta:
        model = Order
        fields = ['id', 'user', 'created_at', 'status', 'total_price',
                  'items']
