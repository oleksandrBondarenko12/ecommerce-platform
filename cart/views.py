# In cart/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Cart, CartItem, Product
from .serializers import CartSerializer


class CartView(APIView):
    # Only authenticated users can access their cart.
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        """
        Retrieve the current user's shopping cart.
        Creates a cart if one doesn't exist for the user.
        """
        # `get_or_create` is a handy Django shortcut.
        # It tries to get the cart for the user, and if it doesn't exist,
        # it creates one. It returns a tuple: (object, created_boolean).
        cart, created = Cart.objects.get_or_create(user=request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        """
        Add a product to the cart or update its quantity.
        Expects a JSON body with 'product_id' and 'quantity'.
        """
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity', 1)

        if not product_id:
            return Response({"error": "Product ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({"error": "Product not found."}, status=status.HTTP_404_NOT_FOUND)

        # Get or create the user's cart.
        cart, _ = Cart.objects.get_or_create(user=request.user)

        # Get or create the cart item.
        # This will update the quantity if the item is already in the cart.
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart, 
            product=product,
            # `defaults` is used for the fields to set if a new object is created.
            defaults={'quantity': quantity}
        )

        # If the item was not created (it already existed), update its quantity.
        if not created:
            cart_item.quantity += int(quantity)
            cart_item.save()

        serializer = CartSerializer(cart)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        """
        Remove a product from the cart.
        Expects a JSON body with 'product_id'.
        """
        product_id = request.data.get('product_id')

        if not product_id:
            return Response({"error": "Product ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Get the cart and the specific item to delete.
            cart = Cart.objects.get(user=request.user)
            cart_item = CartItem.objects.get(cart=cart, product_id=product_id)
            cart_item.delete()
            
            serializer = CartSerializer(cart)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Cart.DoesNotExist:
            return Response({"error": "Cart not found."}, status=status.HTTP_404_NOT_FOUND)
        except CartItem.DoesNotExist:
            return Response({"error": "Item not found in cart."}, status=status.HTTP_404_NOT_FOUND)
