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
        This method is idempotent: it SETS the quantity of a product.
        Expects a JSON body with 'product_id' and 'quantity'.
        """
        product_id = request.data.get('product_id')

        # Validate quantity to ensure it's a positive integer.
        try:
            quantity = int(request.data.get('quantity', 1))
            if quantity <= 0:
                return Response(
                    {"error": "Quantity must be a positive integer."},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except (ValueError, TypeError):
            return Response(
                {"error": "Invalid quantity provided."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not product_id:
            return Response({"error": "Product ID is required."},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({"error": "Product not found."},
                            status=status.HTTP_404_NOT_FOUND)

        # Get or create the user's cart.
        cart, _ = Cart.objects.get_or_create(user=request.user)

        # Use update_or_create to simplify the logic.
        # This creates a new CartItem
        # or updates the quantity of an existing one.
        cart_item, created = CartItem.objects.update_or_create(
            cart=cart,
            product=product,
            defaults={'quantity': quantity}
        )

        # Return 201 Created for a new item, 200 OK for an updated one.
        status_code = status.HTTP_201_CREATED if created else status.HTTP_200_OK
        serializer = CartSerializer(cart)
        return Response(serializer.data, status=status_code)

    def delete(self, request, *args, **kwargs):
        """
        Remove a product from the cart entirely.
        Expects a JSON body with 'product_id'.
        """
        product_id = request.data.get('product_id')

        if not product_id:
            return Response({"error": "Product ID is required."},
                            status=status.HTTP_400_BAD_REQUEST)

        # Find the specific item belonging to the current user's cart.
        # This is more efficient and secure than fetching the cart first.
        cart_item = CartItem.objects.filter(
            cart__user=request.user,
            product_id=product_id
        ).first()

        if not cart_item:
            return Response({"error": "Item not found in cart."},
                            status=status.HTTP_404_NOT_FOUND)

        cart_item.delete()

        # A 204 No Content response is standard for a successful DELETE,
        # indicating success without sending a response body.
        return Response(status=status.HTTP_204_NO_CONTENT)

