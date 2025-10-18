from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ProductForm
from .models import Product


def product_list(request):
    products = Product.objects.select_related('category').order_by('-created_at')

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, f"Product '{product.name}' was added successfully.")
            return redirect('product_list')
        else:
            messages.error(request, 'Please correct the errors below to add the product.')
    else:
        form = ProductForm()

    context = {
        'products': products,
        'form': form,
    }
    return render(request, 'products/product_list.html', context)


def product_detail(request, product_id):
    product = get_object_or_404(Product, product_id=product_id)
    return render(request, 'products/product_detail.html', {'product': product})
