from django.shortcuts import render
# In orders/views.py
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.db import transaction
from .models import Order, OrderItem
from cart.models import Cart
from .serializers import OrderSerializer


class OrderCreateView(generics.CreateAPIView):
    """
    Create a new order from the user's current cart.
    """
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        try:
            cart = Cart.objects.get(user=request.user)
            cart_items = cart.items.all()
            if not cart_items.exists():
                return Response({"error": "Your cart is empty."}, status=status.HTTP_400_BAD_REQUEST)

            # Use a database transaction to ensure all or nothing
            with transaction.atomic():
                # 1. Create the Order
                order = Order.objects.create(
                    user=request.user,
                    total_price=sum(item.product.price * item.quantity for item in cart_items)
                )

                # 2. Create OrderItems from CartItems
                order_items_to_create = []
                for item in cart_items:
                    order_items_to_create.append(
                        OrderItem(
                            order=order,
                            product=item.product,
                            quantity=item.quantity,
                            price_at_purchase=item.product.price # Take a snapshot of the price
                        )
                    )
                OrderItem.objects.bulk_create(order_items_to_create)

                # 3. Clear the cart
                cart.items.all().delete()

            serializer = self.get_serializer(order)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

        except Cart.DoesNotExist:
            return Response({"error": "You do not have a cart."}, status=status.HTTP_400_BAD_REQUEST)


class OrderHistoryView(generics.ListAPIView):
    """
    List all orders for the current authenticated user.
    """
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by('-created_at')

