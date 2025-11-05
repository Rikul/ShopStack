"""
Seed data script for ShopStack ecommerce application.
Run this script to populate the database with sample data for development/testing.

Usage:
    python manage.py shell < seed_data.py
    OR
    python seed_data.py (if Django environment is set up)
"""

import os
import django
from decimal import Decimal
from datetime import datetime, timedelta
import random

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')
django.setup()

from accounts.models import User, Customer
from products.models import Category, Product
from orders.models import Order, OrderItem
from payments.models import Payment


def clear_existing_data():
    """Clear all existing data from the database."""
    print("Clearing existing data...")
    Payment.objects.all().delete()
    OrderItem.objects.all().delete()
    Order.objects.all().delete()
    Product.objects.all().delete()
    Category.objects.all().delete()
    Customer.objects.all().delete()
    User.objects.filter(is_superuser=False).delete()
    print("Existing data cleared.\n")


def create_users():
    """Create sample users."""
    print("Creating users...")
    users = []

    # Create sample users
    user_data = [
        {
            'username': 'john_doe',
            'email': 'john@example.com',
            'first_name': 'John',
            'last_name': 'Doe',
            'phone_number': '555-0101',
            'address': '123 Main St, New York, NY 10001'
        },
        {
            'username': 'jane_smith',
            'email': 'jane@example.com',
            'first_name': 'Jane',
            'last_name': 'Smith',
            'phone_number': '555-0102',
            'address': '456 Oak Ave, Los Angeles, CA 90001'
        },
        {
            'username': 'bob_johnson',
            'email': 'bob@example.com',
            'first_name': 'Bob',
            'last_name': 'Johnson',
            'phone_number': '555-0103',
            'address': '789 Pine Rd, Chicago, IL 60601'
        },
        {
            'username': 'alice_williams',
            'email': 'alice@example.com',
            'first_name': 'Alice',
            'last_name': 'Williams',
            'phone_number': '555-0104',
            'address': '321 Elm St, Houston, TX 77001'
        },
        {
            'username': 'charlie_brown',
            'email': 'charlie@example.com',
            'first_name': 'Charlie',
            'last_name': 'Brown',
            'phone_number': '555-0105',
            'address': '654 Maple Dr, Phoenix, AZ 85001'
        }
    ]

    for data in user_data:
        user = User.objects.create_user(
            username=data['username'],
            email=data['email'],
            password='password123',
            first_name=data['first_name'],
            last_name=data['last_name'],
            phone_number=data['phone_number'],
            address=data['address']
        )
        users.append(user)
        print(f"  Created user: {user.username}")

    print(f"Created {len(users)} users.\n")
    return users


def create_customers():
    """Create sample customers."""
    print("Creating customers...")
    customers = []

    customer_data = [
        {
            'username': 'sarah_connor',
            'email': 'sarah@example.com',
            'first_name': 'Sarah',
            'last_name': 'Connor',
            'phone_number': '555-0201',
            'address': '111 Tech Blvd, San Francisco, CA 94102'
        },
        {
            'username': 'mike_ross',
            'email': 'mike@example.com',
            'first_name': 'Mike',
            'last_name': 'Ross',
            'phone_number': '555-0202',
            'address': '222 Legal Ave, Boston, MA 02101'
        },
        {
            'username': 'emma_watson',
            'email': 'emma@example.com',
            'first_name': 'Emma',
            'last_name': 'Watson',
            'phone_number': '555-0203',
            'address': '333 Star Lane, Seattle, WA 98101'
        },
        {
            'username': 'david_miller',
            'email': 'david@example.com',
            'first_name': 'David',
            'last_name': 'Miller',
            'phone_number': '555-0204',
            'address': '444 Business St, Miami, FL 33101'
        },
        {
            'username': 'lisa_anderson',
            'email': 'lisa@example.com',
            'first_name': 'Lisa',
            'last_name': 'Anderson',
            'phone_number': '555-0205',
            'address': '555 Garden Way, Denver, CO 80201'
        }
    ]

    for data in customer_data:
        customer = Customer.objects.create(
            username=data['username'],
            email=data['email'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            phone_number=data['phone_number'],
            address=data['address']
        )
        customer.set_password('password123')
        customer.save()
        customers.append(customer)
        print(f"  Created customer: {customer.username}")

    print(f"Created {len(customers)} customers.\n")
    return customers


def create_categories():
    """Create product categories."""
    print("Creating categories...")
    categories = []

    category_data = [
        {
            'name': 'Electronics',
            'description': 'Electronic devices and accessories'
        },
        {
            'name': 'Clothing',
            'description': 'Apparel and fashion items'
        },
        {
            'name': 'Books',
            'description': 'Physical and digital books'
        },
        {
            'name': 'Home & Garden',
            'description': 'Home improvement and garden supplies'
        },
        {
            'name': 'Sports & Outdoors',
            'description': 'Sporting goods and outdoor equipment'
        },
        {
            'name': 'Toys & Games',
            'description': 'Toys, games, and hobby items'
        },
        {
            'name': 'Food & Beverages',
            'description': 'Groceries and gourmet foods'
        }
    ]

    for data in category_data:
        category = Category.objects.create(**data)
        categories.append(category)
        print(f"  Created category: {category.name}")

    print(f"Created {len(categories)} categories.\n")
    return categories


def create_products(categories):
    """Create sample products."""
    print("Creating products...")
    products = []

    product_data = [
        # Electronics
        {
            'name': 'Wireless Bluetooth Headphones',
            'description': 'Premium noise-cancelling wireless headphones with 30-hour battery life',
            'price': Decimal('149.99'),
            'category': 'Electronics',
            'stock_quantity': 50
        },
        {
            'name': 'Smart Watch Series 5',
            'description': 'Feature-rich smartwatch with health tracking and GPS',
            'price': Decimal('299.99'),
            'category': 'Electronics',
            'stock_quantity': 30
        },
        {
            'name': 'Laptop Stand Aluminum',
            'description': 'Ergonomic aluminum laptop stand with adjustable height',
            'price': Decimal('39.99'),
            'category': 'Electronics',
            'stock_quantity': 100
        },
        {
            'name': '4K Webcam',
            'description': 'Ultra HD webcam with auto-focus and noise-cancelling mic',
            'price': Decimal('89.99'),
            'category': 'Electronics',
            'stock_quantity': 45
        },
        # Clothing
        {
            'name': 'Cotton T-Shirt (3-Pack)',
            'description': 'Comfortable 100% cotton t-shirts in assorted colors',
            'price': Decimal('29.99'),
            'category': 'Clothing',
            'stock_quantity': 200
        },
        {
            'name': 'Denim Jeans',
            'description': 'Classic fit denim jeans with stretch comfort',
            'price': Decimal('59.99'),
            'category': 'Clothing',
            'stock_quantity': 80
        },
        {
            'name': 'Winter Jacket',
            'description': 'Waterproof winter jacket with insulated lining',
            'price': Decimal('129.99'),
            'category': 'Clothing',
            'stock_quantity': 40
        },
        # Books
        {
            'name': 'Python Programming Masterclass',
            'description': 'Comprehensive guide to Python programming for all levels',
            'price': Decimal('44.99'),
            'category': 'Books',
            'stock_quantity': 75
        },
        {
            'name': 'The Art of Web Design',
            'description': 'Modern web design principles and best practices',
            'price': Decimal('39.99'),
            'category': 'Books',
            'stock_quantity': 60
        },
        {
            'name': 'Cooking Made Easy',
            'description': '500+ recipes for everyday cooking',
            'price': Decimal('24.99'),
            'category': 'Books',
            'stock_quantity': 90
        },
        # Home & Garden
        {
            'name': 'LED Desk Lamp',
            'description': 'Adjustable LED desk lamp with USB charging port',
            'price': Decimal('34.99'),
            'category': 'Home & Garden',
            'stock_quantity': 120
        },
        {
            'name': 'Indoor Plant Set (5-Pack)',
            'description': 'Collection of easy-care indoor plants',
            'price': Decimal('49.99'),
            'category': 'Home & Garden',
            'stock_quantity': 55
        },
        {
            'name': 'Storage Bins Set',
            'description': 'Stackable storage bins with lids (Set of 6)',
            'price': Decimal('29.99'),
            'category': 'Home & Garden',
            'stock_quantity': 85
        },
        # Sports & Outdoors
        {
            'name': 'Yoga Mat Premium',
            'description': 'Non-slip yoga mat with carrying strap',
            'price': Decimal('34.99'),
            'category': 'Sports & Outdoors',
            'stock_quantity': 110
        },
        {
            'name': 'Camping Tent 4-Person',
            'description': 'Waterproof tent with easy setup for 4 people',
            'price': Decimal('159.99'),
            'category': 'Sports & Outdoors',
            'stock_quantity': 25
        },
        {
            'name': 'Resistance Bands Set',
            'description': 'Complete resistance band set with multiple resistance levels',
            'price': Decimal('24.99'),
            'category': 'Sports & Outdoors',
            'stock_quantity': 95
        },
        # Toys & Games
        {
            'name': 'Board Game: Strategy Master',
            'description': 'Engaging strategy board game for 2-6 players',
            'price': Decimal('39.99'),
            'category': 'Toys & Games',
            'stock_quantity': 70
        },
        {
            'name': 'Building Blocks Set',
            'description': '500-piece building blocks set with storage box',
            'price': Decimal('44.99'),
            'category': 'Toys & Games',
            'stock_quantity': 65
        },
        # Food & Beverages
        {
            'name': 'Organic Coffee Beans (2lb)',
            'description': 'Premium organic whole bean coffee',
            'price': Decimal('19.99'),
            'category': 'Food & Beverages',
            'stock_quantity': 150
        },
        {
            'name': 'Green Tea Variety Pack',
            'description': 'Assorted green tea flavors (40 bags)',
            'price': Decimal('14.99'),
            'category': 'Food & Beverages',
            'stock_quantity': 130
        }
    ]

    category_dict = {cat.name: cat for cat in categories}

    for data in product_data:
        category_name = data.pop('category')
        product = Product.objects.create(
            category=category_dict[category_name],
            **data
        )
        products.append(product)
        print(f"  Created product: {product.name} - ${product.price}")

    print(f"Created {len(products)} products.\n")
    return products


def create_orders(customers, products):
    """Create sample orders with order items."""
    print("Creating orders...")
    orders = []

    statuses = ['pending', 'processing', 'shipped', 'delivered', 'cancelled']

    for i, customer in enumerate(customers):
        # Create 1-3 orders per customer
        num_orders = random.randint(1, 3)

        for j in range(num_orders):
            # Select random products for this order
            num_items = random.randint(1, 5)
            selected_products = random.sample(products, num_items)

            # Calculate total amount
            total_amount = Decimal('0.00')
            order_items_data = []

            for product in selected_products:
                quantity = random.randint(1, 3)
                price = product.price
                total_amount += price * quantity
                order_items_data.append({
                    'product': product,
                    'quantity': quantity,
                    'price': price
                })

            # Create order
            order = Order.objects.create(
                customer=customer,
                total_amount=total_amount,
                status=random.choice(statuses)
            )

            # Create order items
            for item_data in order_items_data:
                OrderItem.objects.create(
                    order=order,
                    **item_data
                )

            orders.append(order)
            print(f"  Created order #{order.order_id} for {customer.username} - ${order.total_amount} ({order.items.count()} items)")

    print(f"Created {len(orders)} orders.\n")
    return orders


def create_payments(orders):
    """Create sample payments for orders."""
    print("Creating payments...")
    payments = []

    payment_methods = ['credit_card', 'paypal', 'bank_transfer']
    payment_statuses = ['pending', 'completed', 'failed', 'refunded']

    for order in orders:
        # Most orders have 1 payment, some have 2 (failed then successful)
        num_payments = 1 if random.random() > 0.2 else 2

        for i in range(num_payments):
            # First payment might fail, second should succeed
            if num_payments == 2:
                status = 'failed' if i == 0 else 'completed'
            else:
                # Single payment - mostly completed, some pending or failed
                if order.status == 'cancelled':
                    status = 'refunded' if random.random() > 0.5 else 'failed'
                elif order.status == 'pending':
                    status = 'pending'
                else:
                    status = random.choices(
                        ['completed', 'pending', 'failed'],
                        weights=[0.8, 0.1, 0.1]
                    )[0]

            # Generate unique transaction ID
            transaction_id = f"TXN-{datetime.now().strftime('%Y%m%d')}-{order.order_id:04d}-{i+1}"

            payment = Payment.objects.create(
                order=order,
                payment_method=random.choice(payment_methods),
                amount=order.total_amount,
                transaction_id=transaction_id,
                status=status,
                notes=f"Payment attempt {i+1} for order #{order.order_id}"
            )
            payments.append(payment)
            print(f"  Created payment #{payment.payment_id} for Order #{order.order_id} - {status}")

    print(f"Created {len(payments)} payments.\n")
    return payments


def print_summary(users, customers, categories, products, orders, payments):
    """Print summary of created data."""
    print("\n" + "="*60)
    print("DATABASE SEEDING COMPLETED SUCCESSFULLY")
    print("="*60)
    print(f"\nSummary:")
    print(f"  - Users: {len(users)}")
    print(f"  - Customers: {len(customers)}")
    print(f"  - Categories: {len(categories)}")
    print(f"  - Products: {len(products)}")
    print(f"  - Orders: {len(orders)}")
    print(f"  - Order Items: {sum(order.items.count() for order in orders)}")
    print(f"  - Payments: {len(payments)}")
    print(f"\nTest Credentials:")
    print(f"  Users: username/password123 (e.g., john_doe/password123)")
    print(f"  Customers: username/password123 (e.g., sarah_connor/password123)")
    print("\n" + "="*60 + "\n")


def main():
    """Main function to run all seed operations."""
    print("\n" + "="*60)
    print("SHOPSTACK DATABASE SEEDING")
    print("="*60 + "\n")

    # Ask for confirmation
    response = input("This will delete all existing data. Continue? (yes/no): ")
    if response.lower() not in ['yes', 'y']:
        print("Operation cancelled.")
        return

    print()

    # Run seeding operations
    clear_existing_data()
    users = create_users()
    customers = create_customers()
    categories = create_categories()
    products = create_products(categories)
    orders = create_orders(customers, products)
    payments = create_payments(orders)

    # Print summary
    print_summary(users, customers, categories, products, orders, payments)


if __name__ == '__main__':
    main()
