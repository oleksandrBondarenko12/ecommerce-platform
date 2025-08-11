from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from products.models import Product, Category
from cart.models import Cart
from .models import Order, OrderItem


class OrderCreationTestCase(APITestCase):
    """ 
    Test suite for the order creating process.
    """

    def setUp(self):
        """
        This method runs before any tests in this class. We will set up a user,
        a product, and a cart here.
        """
        self.user = User.objects.create(username='testuser',
                                        password='testpassword123')

        self.category = Category.objects.create(name='Testing Category')
        self.product = Product.objects.create(
            name='Test Product',
            category=self.category,
            price=10.00
        )

        # Log the user in for all subsequent requests in this test case
        self.client.force_authenticate(user=self.user)

    def test_create_order_from_cart(self):
        """
        Ensures an order can be sucessfully creatd from a user's cart,
        and that the cart is cleared afterward.
        """
        # --- ARRANGE ---
        # Get the user's cart and add an item to it
        cart = Cart.objects.create(user=self.user)
        cart.items.create(product=self.product, quantity=2)

        # Verify initial state before the API call
        self.assertEqual(Order.objects.count(), 0)
        self.assertEqual(cart.items.count(), 1)

        # --- ACT ---
        # 2. Make a POST request to the order creating endpoint.
        response = self.client.post('/api/orders/', {}, format='json')

        # --- ASSERT ---
        # 3. Check the results.

        # Check that the API returned a '201 Created' status
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check that one Order object was created in the database
        self.assertEqual(Order.objects.count(), 1)

        # Get the newly created order
        order = Order.objects.first()

        # Check the order belongs to the correct user
        self.assertEqual(order.user, self.user)

        # Check that the order has one OrderItem
        self.assertEqual(order.items.count(), 1)

        # Get the order item and check its details
        order_item = order.items.first()
        self.assertEqual(order_item.product, self.product)
        self.assertEqual(order_item.quantity, 2)
        self.assertEqual(order_item.price_at_purchase, self.product.price)
        
        # Check that the order's total price is correct (2 * 10.00)
        self.assertEqual(order.total_price, 20.00)

        # 4. CRUCIAL: Check that the cart is now empty.
        cart.refresh_from_db() # Refresh the cart object from the database
        self.assertEqual(cart.items.count(), 0)

