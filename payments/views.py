# In payments/views.py
from rest_framework import views, response, status, permissions
from django.core.mail import send_mail  # <-- REMOVE 'outbox' from this import
from django.conf import settings
from orders.models import Order


class MockPaymentView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        order_id = request.data.get('order_id')

        if not order_id:
            return response.Response({"error": "Order ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            order = Order.objects.get(id=order_id, user=request.user)
        except Order.DoesNotExist:
            return response.Response({"error": "Order not found."}, status=status.HTTP_404_NOT_FOUND)

        if order.status == Order.OrderStatus.PAID:
            return response.Response({"message": "This order has already been paid."}, status=status.HTTP_200_OK)
        
        print(f"Simulating successful payment for Order ID: {order.id}...")
        
        order.status = Order.OrderStatus.PAID
        order.save()

        # --- Send Notification Email ---
        self.send_order_confirmation_email(order)
        
        return response.Response({
            "message": "Payment successful. Order is now marked as PAID.",
            "order_id": order.id,
            "status": order.status
        }, status=status.HTTP_200_OK)

    def send_order_confirmation_email(self, order):
        subject = f"Your Order Confirmation #{order.id}"
        message = (
            f"Hello {order.user.username},\n\n"
            f"Thank you for your purchase! Your order #{order.id} has been paid and is being processed."
        )
        
        try:
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[order.user.email],
                fail_silently=False,
            )
            print(f"Confirmation email for Order ID: {order.id} was generated for the console.")
        except Exception as e:
            # Add error logging for any unexpected email issues
            print(f"Error sending email for Order ID {order.id}: {e}")
