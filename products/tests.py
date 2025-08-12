from django.test import TestCase
# In products/tests.py
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
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Laptop')
# Create your tests here.

