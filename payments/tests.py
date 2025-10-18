from django.contrib.auth import get_user_model
from django.test import TestCase

from orders.models import Order
from products.models import Category, Product

from .models import Payment


class PaymentModelTest(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(
            username='paymenttester',
            email='paymenttester@example.com',
            password='testpassword'
        )
        self.category = Category.objects.create(
            name='Services',
            description='Service offerings'
        )
        self.product = Product.objects.create(
            name='Consulting Hours',
            description='Professional services package',
            price=100.00,
            stock_quantity=10,
            category=self.category
        )
        self.order = Order.objects.create(
            user=self.user,
            total_amount=100.00,
            status='pending'
        )
        self.payment = Payment.objects.create(
            order=self.order,
            payment_method='credit_card',
            amount=100.00,
            transaction_id='txn_123456',
            status='completed'
        )

    def test_payment_creation(self):
        self.assertEqual(self.payment.order, self.order)
        self.assertEqual(self.payment.payment_method, 'credit_card')
        self.assertEqual(self.payment.amount, 100.00)
        self.assertEqual(self.payment.transaction_id, 'txn_123456')
        self.assertEqual(self.payment.status, 'completed')

    def test_payment_str(self):
        self.assertEqual(str(self.payment), f'Payment #{self.payment.payment_id} for Order #{self.order.order_id}')