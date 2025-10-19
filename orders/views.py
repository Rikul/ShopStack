from decimal import Decimal

from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import OrderForm, OrderItemFormSet
from .models import Order
from products.models import Product


@staff_member_required
def admin_orders(request):
    """Admin view for managing all orders"""
    orders = Order.objects.select_related('customer').prefetch_related('items__product').order_by('-created_at')
    
    # Filter by status if requested
    status_filter = request.GET.get('status')
    if status_filter:
        orders = orders.filter(status=status_filter)
    
    # Search functionality
    search_query = request.GET.get('search')
    if search_query:
        orders = orders.filter(
            Q(order_id__icontains=search_query) |
            Q(customer__username__icontains=search_query) |
            Q(customer__email__icontains=search_query)
        )
    
    product_filter = request.GET.get('product')
    product_reference = None
    if product_filter:
        orders = orders.filter(items__product__product_id=product_filter).distinct()
        try:
            product_reference = Product.objects.get(product_id=product_filter)
        except (Product.DoesNotExist, ValueError):
            product_reference = None

    context = {
        'orders': orders,
        'status_filter': status_filter,
        'search_query': search_query,
        'product_filter': product_filter,
        'product_reference': product_reference,
        'order_statuses': Order.objects.values_list('status', flat=True).distinct(),
    }
    return render(request, 'orders/admin_orders.html', context)

@staff_member_required
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

@staff_member_required
def admin_order_create(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        provisional_order = Order()
        formset = OrderItemFormSet(request.POST, instance=provisional_order, prefix='items')

        if form.is_valid() and formset.is_valid():
            order = form.save(commit=False)
            order.total_amount = Decimal('0.00')
            order.save()

            formset.instance = order
            total_amount = Decimal('0.00')
            order_items = formset.save(commit=False)
            for item in order_items:
                item.price = item.product.price
                item.save()
                total_amount += item.price * item.quantity

            order.total_amount = total_amount
            order.save()

            messages.success(request, 'Order created successfully.')
            return redirect('admin_order_detail', order_id=order.order_id)
    else:
        form = OrderForm()
        formset = OrderItemFormSet(instance=Order(), prefix='items')

    context = {
        'form': form,
        'formset': formset,
    }
    return render(request, 'orders/admin_order_create.html', context)