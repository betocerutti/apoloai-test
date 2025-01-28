from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from .models import Product


class ProductTests(APITestCase):
    def setUp(self):
        """
        Set up test data.
        """
        self.client = APIClient()
        self.product1 = Product.objects.create(name="Apple", price="1.20", stock=100)
        self.product2 = Product.objects.create(name="Banana", price="0.50", stock=150)

    def test_list_products(self):
        """
        Test listing all products.
        """
        url = reverse(
            "product-list"
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Check that 2 products are returned

    def test_retrieve_single_product(self):
        """
        Test retrieving a single product by ID.
        """
        url = reverse(
            "product-detail", args=[self.product1.id]
        ) 
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Apple")  # Check the product name
        self.assertEqual(response.data["price"], "1.20")  # Check the product price
        self.assertEqual(response.data["stock"], 100)  # Check the product stock

    def test_update_stock_success(self):
        """
        Test updating the stock of a product successfully.
        """
        url = reverse(
            "product-update-stock", args=[self.product1.id]
        )
        data = {"stock": 50}
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["stock"], 50)  # Check that the stock was updated

        # Verify the stock was updated in the database
        updated_product = Product.objects.get(id=self.product1.id)
        self.assertEqual(updated_product.stock, 50)

    def test_update_stock_missing_stock(self):
        """
        Test updating the stock of a product with missing stock value.
        """
        url = reverse("product-update-stock", args=[self.product1.id])
        data = {}  # Missing stock field
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["error"], "stock is required"
        )  # Check the error message

    def test_update_stock_invalid_product(self):
        """
        Test updating the stock of a non-existent product.
        """
        invalid_product_id = 999  # Non-existent product ID
        url = reverse("product-update-stock", args=[invalid_product_id])
        data = {"stock": 50}
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            response.data["detail"], "No Product matches the given query."
        )  # Check the error message
