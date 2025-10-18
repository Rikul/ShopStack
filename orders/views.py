from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Order, OrderItem
from products.models import Product

@login_required
def admin_orders(request):
    """Admin view for managing all orders"""
    orders = Order.objects.select_related('user').prefetch_related('items__product').order_by('-created_at')
    
    # Filter by status if requested
    status_filter = request.GET.get('status')
    if status_filter:
        orders = orders.filter(status=status_filter)
    
    # Search functionality
    search_query = request.GET.get('search')
    if search_query:
        orders = orders.filter(
            Q(order_id__icontains=search_query) |
            Q(user__username__icontains=search_query) |
            Q(user__email__icontains=search_query)
        )
    
    context = {
        'orders': orders,
        'status_filter': status_filter,
        'search_query': search_query,
        'order_statuses': Order.objects.values_list('status', flat=True).distinct(),
    }
    return render(request, 'orders/admin_orders.html', context)

@login_required
def admin_order_detail(request, order_id):
    """Admin view for order details"""
    order = get_object_or_404(Order, order_id=order_id)
    
    if request.method == 'POST':
        # Update order status
        new_status = request.POST.get('status')
        if new_status in ['pending', 'processing', 'shipped', 'delivered', 'cancelled']:
            order.status = new_status
            order.save()
            messages.success(request, f'Order status updated to {new_status.title()}')
            return redirect('admin_order_detail', order_id=order_id)
    
    context = {
        'order': order,
        'order_items': order.items.select_related('product'),
    }
    return render(request, 'orders/admin_order_detail.html', context)

@login_required
def cart_view(request):
    order, created = Order.objects.get_or_create(user=request.user, status='pending')
    order_items = OrderItem.objects.filter(order=order)
    total_amount = sum(item.price * item.quantity for item in order_items)
    
    context = {
        'cart_items': order_items,
        'total_amount': total_amount,
    }
    return render(request, 'orders/cart.html', context)

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, product_id=product_id)
    
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        
        # Check stock availability
        if quantity > product.stock_quantity:
            messages.error(request, f'Only {product.stock_quantity} items available in stock.')
            return redirect('product_detail', product_id=product_id)
        
        # Get or create pending order
        order, created = Order.objects.get_or_create(
            user=request.user, 
            status='pending',
            defaults={'total_amount': 0}
        )
        
        # Check if item already in cart
        order_item, item_created = OrderItem.objects.get_or_create(
            order=order,
            product=product,
            defaults={'quantity': quantity, 'price': product.price}
        )
        
        if not item_created:
            # Update quantity if item already exists
            order_item.quantity += quantity
            order_item.save()
        
        # Update order total
        order.total_amount = sum(item.price * item.quantity for item in order.items.all())
        order.save()
        
        messages.success(request, f'{product.name} added to cart successfully!')
        return redirect('cart')
    
    return redirect('product_detail', product_id=product_id)

@login_required
def remove_from_cart(request, item_id):
    order_item = get_object_or_404(OrderItem, order_item_id=item_id, order__user=request.user)
    product_name = order_item.product.name
    
    # Remove the item
    order_item.delete()
    
    # Update order total
    order = order_item.order
    order.total_amount = sum(item.price * item.quantity for item in order.items.all())
    order.save()
    
    messages.success(request, f'{product_name} removed from cart.')
    return redirect('cart')

@login_required
def checkout_view(request):
    order, created = Order.objects.get_or_create(user=request.user, status='pending')
    order_items = OrderItem.objects.filter(order=order)
    
    if not order_items.exists():
        messages.warning(request, 'Your cart is empty.')
        return redirect('cart')
    
    if request.method == 'POST':
        # Process the order and payment here
        order.status = 'processing'
        order.save()
        messages.success(request, 'Order placed successfully!')
        return redirect('dashboard:dashboard')  # Redirect to dashboard

    context = {
        'order_items': order_items,
        'total_amount': sum(item.price * item.quantity for item in order_items),
    }
    return render(request, 'orders/checkout.html', context)