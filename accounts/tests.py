from django.test import TestCase
from django.urls import reverse

from .models import Customer, User


class UserModelTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpassword'
        )

    def test_user_creation(self):
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.email, 'testuser@example.com')


class CustomerModelTests(TestCase):

    def test_customer_creation(self):
        customer = Customer(
            username='customer',
            email='customer@example.com',
            first_name='Test',
            last_name='Customer'
        )
        customer.set_password('securepass')
        customer.save()

        self.assertTrue(customer.check_password('securepass'))
        self.assertEqual(customer.get_full_name(), 'Test Customer')
        self.assertTrue(customer.is_active)


class UserViewsTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpassword'
        )
        self.user.is_staff = True
        self.user.save()

    def test_login_view(self):
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'testpassword'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('dashboard:dashboard'))

    def test_login_rejects_non_staff_user(self):
        User.objects.create_user(
            username='regularuser',
            email='regular@example.com',
            password='regularpassword'
        )
        response = self.client.post(reverse('login'), {
            'username': 'regularuser',
            'password': 'regularpassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Access is restricted to staff members')
