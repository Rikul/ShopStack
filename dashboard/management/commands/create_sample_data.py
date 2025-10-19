from django.core.management.base import BaseCommand
from products.models import Category, Product
from orders.models import Order, OrderItem
from decimal import Decimal
import random
from datetime import timedelta
from django.utils import timezone
from accounts.models import Customer

class Command(BaseCommand):
    help = 'Create sample data for the dashboard'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample data...')
        
        # Create sample categories
        categories_data = [
            {'name': 'Electronics', 'description': 'Electronic devices and gadgets'},
            {'name': 'Clothing', 'description': 'Fashion and apparel'},
            {'name': 'Books', 'description': 'Books and literature'},
            {'name': 'Home & Garden', 'description': 'Home improvement and gardening'},
            {'name': 'Sports', 'description': 'Sports equipment and gear'},
        ]
        
        categories = []
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={'description': cat_data['description']}
            )
            categories.append(category)
            if created:
                self.stdout.write(f'Created category: {category.name}')
        
        # Create sample products
        products_data = [
            # Electronics
            {'name': 'Smartphone Pro', 'price': Decimal('899.99'), 'stock': 25, 'category': 'Electronics'},
            {'name': 'Laptop Ultra', 'price': Decimal('1299.99'), 'stock': 15, 'category': 'Electronics'},
            {'name': 'Wireless Headphones', 'price': Decimal('199.99'), 'stock': 50, 'category': 'Electronics'},
            {'name': 'Smart Watch', 'price': Decimal('299.99'), 'stock': 8, 'category': 'Electronics'},
            
            # Clothing
            {'name': 'Designer T-Shirt', 'price': Decimal('29.99'), 'stock': 100, 'category': 'Clothing'},
            {'name': 'Jeans Premium', 'price': Decimal('79.99'), 'stock': 45, 'category': 'Clothing'},
            {'name': 'Winter Jacket', 'price': Decimal('149.99'), 'stock': 3, 'category': 'Clothing'},
            {'name': 'Running Shoes', 'price': Decimal('119.99'), 'stock': 0, 'category': 'Clothing'},
            
            # Books
            {'name': 'Python Programming', 'price': Decimal('39.99'), 'stock': 75, 'category': 'Books'},
            {'name': 'Web Development Guide', 'price': Decimal('49.99'), 'stock': 30, 'category': 'Books'},
            {'name': 'Business Strategy', 'price': Decimal('34.99'), 'stock': 60, 'category': 'Books'},
            
            # Home & Garden
            {'name': 'Coffee Maker Deluxe', 'price': Decimal('89.99'), 'stock': 20, 'category': 'Home & Garden'},
            {'name': 'Garden Tool Set', 'price': Decimal('59.99'), 'stock': 5, 'category': 'Home & Garden'},
            {'name': 'LED Desk Lamp', 'price': Decimal('39.99'), 'stock': 35, 'category': 'Home & Garden'},
            
            # Sports
            {'name': 'Yoga Mat Pro', 'price': Decimal('29.99'), 'stock': 40, 'category': 'Sports'},
            {'name': 'Basketball Official', 'price': Decimal('24.99'), 'stock': 2, 'category': 'Sports'},
            {'name': 'Tennis Racket', 'price': Decimal('89.99'), 'stock': 12, 'category': 'Sports'},
        ]
        
        products = []
        for prod_data in products_data:
            category = Category.objects.get(name=prod_data['category'])
            product, created = Product.objects.get_or_create(
                name=prod_data['name'],
                defaults={
                    'description': f"High-quality {prod_data['name'].lower()} from our premium collection.",
                    'price': prod_data['price'],
                    'stock_quantity': prod_data['stock'],
                    'category': category,
                }
            )
            products.append(product)
            if created:
                self.stdout.write(f'Created product: {product.name}')
        
        # Create sample customers if they don't exist
        sample_users = ['john_doe', 'jane_smith', 'mike_johnson', 'sarah_wilson', 'alex_brown']
        customers = []

        for username in sample_users:
            customer, created = Customer.objects.get_or_create(
                username=username,
                defaults={
                    'email': f'{username}@example.com',
                    'first_name': username.split('_')[0].title(),
                    'last_name': username.split('_')[1].title(),
                }
            )
            if created or not customer.password:
                customer.set_password('password123')
                customer.save()
                if created:
                    self.stdout.write(f'Created customer: {customer.username}')
            customers.append(customer)
        
        # Create sample orders
        order_statuses = ['pending', 'processing', 'shipped', 'delivered', 'cancelled']
        
        for i in range(50):
            customer = random.choice(customers)
            status = random.choice(order_statuses)
            
            # Create order with random date within last 90 days
            created_date = timezone.now() - timedelta(days=random.randint(0, 90))
            
            order = Order.objects.create(
                customer=customer,
                status=status,
                total_amount=Decimal('0.00'),
                created_at=created_date
            )
            
            # Add random order items
            num_items = random.randint(1, 5)
            total_amount = Decimal('0.00')
            
            for _ in range(num_items):
                product = random.choice(products)
                quantity = random.randint(1, 3)
                price = product.price
                
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=quantity,
                    price=price
                )
                
                total_amount += price * quantity
            
            order.total_amount = total_amount
            order.save()
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created sample data:\n'
                f'- {len(categories)} categories\n'
                f'- {len(products)} products\n'
                f'- {len(customers)} customers\n'
                f'- 50 orders with order items'
            )
        )