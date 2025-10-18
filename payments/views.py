import csv

from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Q, Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from .forms import AdminPaymentForm
from .models import Payment


@staff_member_required
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


@staff_member_required
def admin_payments_export(request):
    payments = Payment.objects.select_related('order__user').order_by('-created_at')

    status_filter = request.GET.get('status')
    if status_filter:
        payments = payments.filter(status=status_filter)

    search_query = request.GET.get('search')
    if search_query:
        payments = payments.filter(
            Q(payment_id__icontains=search_query)
            | Q(order__order_id__icontains=search_query)
            | Q(order__user__username__icontains=search_query)
        )

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="payments.csv"'

    writer = csv.writer(response)
    writer.writerow([
        'Payment ID',
        'Order ID',
        'Customer',
        'Email',
        'Status',
        'Amount',
        'Method',
        'Created At',
    ])

    for payment in payments:
        order = payment.order
        writer.writerow(
            [
                payment.payment_id,
                order.order_id if order else '',
                order.user.get_full_name() if order and order.user.get_full_name() else (order.user.username if order else ''),
                order.user.email if order else '',
                payment.get_status_display(),
                payment.amount,
                payment.payment_method,
                payment.created_at.isoformat(),
            ]
        )

    return response


@staff_member_required
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


@staff_member_required
def admin_payment_create(request):
    if request.method == 'POST':
        form = AdminPaymentForm(request.POST)
        if form.is_valid():
            payment = form.save()
            messages.success(request, 'Payment recorded successfully.')
            return redirect('admin_payment_detail', payment_id=payment.payment_id)
    else:
        form = AdminPaymentForm()

    return render(request, 'payments/admin_payment_create.html', {'form': form})