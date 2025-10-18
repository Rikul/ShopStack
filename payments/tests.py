from django.test import TestCase
from .models import Payment

class PaymentModelTest(TestCase):
    def setUp(self):
        self.payment = Payment.objects.create(
            order_id=1,
            payment_method='credit_card',
            amount=100.00,
            transaction_id='txn_123456',
            status='completed'
        )

    def test_payment_creation(self):
        self.assertEqual(self.payment.order_id, 1)
        self.assertEqual(self.payment.payment_method, 'credit_card')
        self.assertEqual(self.payment.amount, 100.00)
        self.assertEqual(self.payment.transaction_id, 'txn_123456')
        self.assertEqual(self.payment.status, 'completed')

    def test_payment_str(self):
        self.assertEqual(str(self.payment), f'Payment {self.payment.payment_id}')