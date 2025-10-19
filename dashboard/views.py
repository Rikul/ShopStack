from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count, Sum
from django.utils import timezone
from datetime import timedelta
from products.models import Product, Category
from orders.models import Order

@staff_member_required
def dashboard_view(request):
    """Main dashboard view with overview statistics"""
    
    # Basic statistics
    total_products = Product.objects.count()
    total_categories = Category.objects.count()
    total_orders = Order.objects.count()
    
    # Recent orders (last 30 days)
    thirty_days_ago = timezone.now() - timedelta(days=30)
    recent_orders = Order.objects.filter(created_at__gte=thirty_days_ago).count()
    
    # Revenue calculations
    total_revenue = Order.objects.filter(status='delivered').aggregate(
        total=Sum('total_amount'))['total'] or 0
    
    monthly_revenue = Order.objects.filter(
        status='delivered',
        created_at__gte=thirty_days_ago
    ).aggregate(total=Sum('total_amount'))['total'] or 0
    
    # Order status breakdown
    order_status_stats = Order.objects.values('status').annotate(count=Count('status'))
    
    # Top selling products
    top_products = Product.objects.annotate(
        order_count=Count('orderitem')
    ).order_by('-order_count')[:5]
    
    # Low stock products (less than 10 items)
    low_stock_products = Product.objects.filter(stock_quantity__lt=10)[:5]
    
    # Recent orders
    recent_orders_list = Order.objects.select_related('customer').order_by('-created_at')[:5]
    
    context = {
        'total_products': total_products,
        'total_categories': total_categories,
        'total_orders': total_orders,
        'recent_orders': recent_orders,
        'total_revenue': total_revenue,
        'monthly_revenue': monthly_revenue,
        'order_status_stats': order_status_stats,
        'top_products': top_products,
        'low_stock_products': low_stock_products,
        'recent_orders_list': recent_orders_list,
    }
    
    return render(request, 'dashboard/dashboard.html', context)

@staff_member_required
def analytics_view(request):
    """Analytics dashboard with charts and detailed metrics"""
    
    # Sales analytics for the last 7 days
    days_data = []
    for i in range(7):
        date = timezone.now().date() - timedelta(days=i)
        day_orders = Order.objects.filter(
            created_at__date=date,
            status='delivered'
        ).aggregate(
            count=Count('order_id'),
            revenue=Sum('total_amount')
        )
        days_data.append({
            'date': date.strftime('%Y-%m-%d'),
            'orders': day_orders['count'] or 0,
            'revenue': float(day_orders['revenue'] or 0)
        })
    
    days_data.reverse()  # Show oldest to newest
    
    # Category performance
    category_stats = Category.objects.annotate(
        product_count=Count('products'),
        total_sold=Count('products__orderitem')
    ).order_by('-total_sold')
    
    # Monthly comparison
    current_month = timezone.now().replace(day=1)
    last_month = (current_month - timedelta(days=1)).replace(day=1)
    
    current_month_stats = Order.objects.filter(
        created_at__gte=current_month,
        status='delivered'
    ).aggregate(
        orders=Count('order_id'),
        revenue=Sum('total_amount')
    )
    
    last_month_stats = Order.objects.filter(
        created_at__gte=last_month,
        created_at__lt=current_month,
        status='delivered'
    ).aggregate(
        orders=Count('order_id'),
        revenue=Sum('total_amount')
    )
    
    context = {
        'days_data': days_data,
        'category_stats': category_stats,
        'current_month_stats': current_month_stats,
        'last_month_stats': last_month_stats,
    }
    
    return render(request, 'dashboard/analytics.html', context)

@staff_member_required
def inventory_view(request):
    """Inventory management dashboard"""
    
    # Stock levels
    products = Product.objects.select_related('category').order_by('stock_quantity')
    
    # Stock alerts
    out_of_stock = Product.objects.filter(stock_quantity=0)
    low_stock = Product.objects.filter(stock_quantity__gt=0, stock_quantity__lt=10)
    
    # Category breakdown
    category_inventory = Category.objects.annotate(
        total_products=Count('products'),
        total_stock=Sum('products__stock_quantity'),
        avg_price=Sum('products__price') / Count('products')
    )
    
    context = {
        'products': products,
        'out_of_stock': out_of_stock,
        'low_stock': low_stock,
        'category_inventory': category_inventory,
    }
    
    return render(request, 'dashboard/inventory.html', context)