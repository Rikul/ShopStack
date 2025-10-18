from django.test import TestCase
from .models import Order, OrderItem
from products.models import Category, Product
from accounts.models import User

class OrderModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpassword'
        )
        self.category = Category.objects.create(
            name='Apparel',
            description='Clothing and accessories'
        )
        self.product = Product.objects.create(
            name='Test Product',
            description='Test Description',
            price=10.00,
            stock_quantity=100,
            category=self.category
        )
        self.order = Order.objects.create(
            user=self.user,
            total_amount=20.00,
            status='pending'
        )
        self.order_item = OrderItem.objects.create(
            order=self.order,
            product=self.product,
            quantity=2,
            price=self.product.price
        )

    def test_order_creation(self):
        self.assertEqual(self.order.user.username, 'testuser')
        self.assertEqual(self.order.total_amount, 20.00)
        self.assertEqual(self.order.status, 'pending')

    def test_order_item_creation(self):
        self.assertEqual(self.order_item.order, self.order)
        self.assertEqual(self.order_item.product.name, 'Test Product')
        self.assertEqual(self.order_item.quantity, 2)
        self.assertEqual(self.order_item.price, 10.00)