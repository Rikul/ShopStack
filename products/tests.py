from django.test import TestCase
from .models import Category, Product

class ProductModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.category = Category.objects.create(
            name='Electronics',
            description='Test category for products'
        )
        cls.product = Product.objects.create(
            name='Test Product',
            description='This is a test product.',
            price=19.99,
            stock_quantity=100,
            category=cls.category
        )

    def test_product_name(self):
        self.assertEqual(self.product.name, 'Test Product')

    def test_product_price(self):
        self.assertEqual(self.product.price, 19.99)

    def test_product_stock_quantity(self):
        self.assertEqual(self.product.stock_quantity, 100)