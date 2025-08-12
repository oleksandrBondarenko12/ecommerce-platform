# In products/tests.py
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Category, Product

class ProductTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.category = Category.objects.create(name='Electronics')
        self.product = Product.objects.create(
            name='Laptop',
            description='A powerful laptop',
            price=1200.00,
            category=self.category
        )

    def test_product_list_api_endpoint(self):
        """Test that the product list endpoint works correctly."""
        url = '/api/products/'
        response = self.client.get(url)

        # Assert that the request was successful (status code 200 OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # --- THIS IS THE FIX ---
        # Assert that the response data is a list containing 1 item.
        self.assertIsInstance(response.data, list)
        self.assertEqual(len(response.data), 1)
        
        # Assert that the product name from the API matches our test product
        self.assertEqual(response.data[0]['name'], 'Laptop')
        print("✅ Passed: Product list API endpoint returns a list with correct data.")

    # Keeping the other tests is good practice!
    def test_category_model_str(self):
        """Unit Test: Test the __str__ representation of the Category model."""
        category = Category.objects.get(name='Electronics')
        self.assertEqual(str(category), 'Electronics')
        print("✅ Passed: Category model __str__ representation.")

    def test_product_model_str(self):
        """Unit Test: Test the __str__ representation of the Product model."""
        product = Product.objects.get(name='Laptop')
        self.assertEqual(str(product), 'Laptop')
        print("✅ Passed: Product model __str__ representation.")

