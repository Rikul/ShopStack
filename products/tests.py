from django.test import TestCase
from .models import Product

class ProductModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Product.objects.create(
            name='Test Product',
            description='This is a test product.',
            price=19.99,
            stock_quantity=100,
            category_id=1
        )

    def test_product_name(self):
        product = Product.objects.get(id=1)
        self.assertEqual(product.name, 'Test Product')

    def test_product_price(self):
        product = Product.objects.get(id=1)
        self.assertEqual(product.price, 19.99)

    def test_product_stock_quantity(self):
        product = Product.objects.get(id=1)
        self.assertEqual(product.stock_quantity, 100)