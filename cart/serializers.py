# In cart/serializers.py

from rest_framework import serializers
from .models import Cart, CartItem
from products.models import Product

# This serializer is just for displaying product info inside the cart item.
# We don't want to show all product details, just the essentials.
class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'price']


# This serializer handles a single item within the cart.
class CartItemSerializer(serializers.ModelSerializer):
    # We use the SimpleProductSerializer to nest product details.
    # `read_only=True` means this nested data is for display only.
    product = SimpleProductSerializer(read_only=True)
    
    # We also need a write-only field to accept the product_id when adding an item.
    product_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'product_id', 'quantity']


# This is the main serializer for the entire shopping cart.
class CartSerializer(serializers.ModelSerializer):
    # 'items' is the `related_name` we set in the CartItem model's ForeignKey.
    # This will nest a list of CartItem objects, serialized by CartItemSerializer.
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        # We only want to display these fields in the final cart view.
        # The 'user' is implicit (the one making the request).
        fields = ['id', 'items', 'total_price']

    def get_total_price(self, cart: Cart):
        # Calculate the total price by summing up the price of each item * quantity.
        # `cart.items.all()` works because of the `related_name='items'` we defined.
        return sum(item.product.price * item.quantity for item in cart.items.all())
