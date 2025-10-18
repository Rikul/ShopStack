from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Sum
from .models import Payment
from orders.models import Order

@login_required
def admin_payments(request):
    """Admin view for managing all payments"""
    payments = Payment.objects.select_related('order__user').order_by('-created_at')
    
    # Filter by status if requested
    status_filter = request.GET.get('status')
    if status_filter:
        payments = payments.filter(status=status_filter)
    
    # Search functionality
    search_query = request.GET.get('search')
    if search_query:
        payments = payments.filter(
            Q(payment_id__icontains=search_query) |
            Q(order__order_id__icontains=search_query) |
            Q(order__user__username__icontains=search_query)
        )
    
    # Calculate summary stats
    total_payments = payments.aggregate(total=Sum('amount'))['total'] or 0
    
    context = {
        'payments': payments,
        'status_filter': status_filter,
        'search_query': search_query,
        'total_payments': total_payments,
        'payment_statuses': Payment.objects.values_list('status', flat=True).distinct(),
    }
    return render(request, 'payments/admin_payments.html', context)

@login_required
def admin_payment_detail(request, payment_id):
    """Admin view for payment details"""
    payment = get_object_or_404(Payment, payment_id=payment_id)
    
    if request.method == 'POST':
        # Update payment status
        new_status = request.POST.get('status')
        if new_status in ['pending', 'completed', 'failed', 'refunded']:
            payment.status = new_status
            payment.save()
            messages.success(request, f'Payment status updated to {new_status.title()}')
            return redirect('admin_payment_detail', payment_id=payment_id)
    
    context = {
        'payment': payment,
    }
    return render(request, 'payments/admin_payment_detail.html', context)

def process_payment(request, order_id):
    if request.method == 'POST':
        order = get_object_or_404(Order, order_id=order_id)
        payment_method = request.POST.get('payment_method')
        amount = order.total_amount
        
        # Create a new payment record
        Payment.objects.create(
            order=order,
            payment_method=payment_method,
            amount=amount,
            status='pending'
        )
        
        messages.success(request, 'Payment processed successfully.')
        return redirect('checkout')
    
    return render(request, 'payments/payment_form.html', {'order_id': order_id})