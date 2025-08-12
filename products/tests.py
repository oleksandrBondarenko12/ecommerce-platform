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

        # Assert that the request was successful
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Assert that the paginated response shows a total count of 1
        self.assertEqual(response.data['count'], 1)
        
        # Assert that the 'results' list contains one item
        self.assertEqual(len(response.data['results']), 1)
        
        # Assert the name of the product inside the 'results' list
        self.assertEqual(response.data['results'][0]['name'], 'Laptop')

