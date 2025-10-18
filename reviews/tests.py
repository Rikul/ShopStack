from django.test import TestCase
from .models import Review
from django.contrib.auth import get_user_model
from products.models import Product

User = get_user_model()

class ReviewModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpassword'
        )
        self.product = Product.objects.create(
            name='Test Product',
            description='Test Description',
            price=10.00,
            stock_quantity=100
        )
        self.review = Review.objects.create(
            user=self.user,
            product=self.product,
            rating=5,
            comment='Great product!'
        )

    def test_review_creation(self):
        self.assertEqual(self.review.user.username, 'testuser')
        self.assertEqual(self.review.product.name, 'Test Product')
        self.assertEqual(self.review.rating, 5)
        self.assertEqual(self.review.comment, 'Great product!')

    def test_review_str(self):
        self.assertEqual(str(self.review), 'Great product!')