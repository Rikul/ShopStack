from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import redirect, render, get_object_or_404
from django.db.models import Q
from .models import User

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_active and user.is_staff:
                login(request, user)
                return redirect('dashboard:dashboard')
            messages.error(request, 'Access is restricted to staff members. Please contact an administrator.')
        else:
            messages.error(request, 'Invalid username or password. Please try again.')
    return render(request, 'accounts/login.html')

@login_required
def profile(request):
    return render(request, 'accounts/profile.html')  # Create a profile.html template for user profile management

# Customer Management Views
@staff_member_required
def customer_list(request):
    """Admin view for managing all customers"""
    customers = User.objects.all().order_by('-date_joined')

    # Search functionality
    search_query = request.GET.get('search')
    if search_query:
        customers = customers.filter(
            Q(username__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(phone_number__icontains=search_query)
        )

    context = {
        'customers': customers,
        'search_query': search_query,
    }
    return render(request, 'accounts/customer_list.html', context)

@staff_member_required
def customer_create(request):
    """Admin view for creating a new customer"""
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone_number = request.POST.get('phone_number', '')
        address = request.POST.get('address', '')
        password = request.POST.get('password')
        is_active = request.POST.get('is_active') == 'on'

        if username and email and password:
            try:
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password,
                    first_name=first_name,
                    last_name=last_name,
                    phone_number=phone_number,
                    address=address,
                    is_staff=False,
                    is_active=is_active
                )
                messages.success(request, f'Customer "{username}" created successfully!')
                return redirect('customer_list')
            except Exception as e:
                messages.error(request, f'Error creating customer: {str(e)}')
        else:
            messages.error(request, 'Username, email, and password are required.')

    return render(request, 'accounts/customer_form.html', {'action': 'Create'})

@staff_member_required
def customer_edit(request, user_id):
    """Admin view for editing a customer"""
    customer = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone_number = request.POST.get('phone_number', '')
        address = request.POST.get('address', '')
        password = request.POST.get('password')
        is_active = request.POST.get('is_active') == 'on'

        if username and email:
            try:
                customer.username = username
                customer.email = email
                customer.first_name = first_name
                customer.last_name = last_name
                customer.phone_number = phone_number
                customer.address = address
                customer.is_active = is_active

                # Only update password if provided
                if password:
                    customer.set_password(password)

                customer.save()
                messages.success(request, f'Customer "{username}" updated successfully!')
                return redirect('customer_list')
            except Exception as e:
                messages.error(request, f'Error updating customer: {str(e)}')
        else:
            messages.error(request, 'Username and email are required.')

    return render(request, 'accounts/customer_form.html', {'customer': customer, 'action': 'Edit'})

@staff_member_required
def customer_delete(request, user_id):
    """Admin view for deleting a customer"""
    customer = get_object_or_404(User, id=user_id)

    # Check if customer can be deleted
    if customer.order_set.count() > 0:
        messages.error(request, f'This customer has {customer.order_set.count()} order(s) and cannot be deleted.')
        return redirect('customer_list')

    if request.method == 'POST':
        username = customer.username
        try:
            customer.delete()
            messages.success(request, f'Customer "{username}" deleted successfully!')
        except Exception as e:
            messages.error(request, f'Error deleting customer: {str(e)}')
        return redirect('customer_list')

    return render(request, 'accounts/customer_confirm_delete.html', {'customer': customer})