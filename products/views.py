from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Product, Category

def product_list(request):
    products = Product.objects.all()
    return render(request, 'products/product_list.html', {'products': products})

def product_detail(request, product_id):
    product = get_object_or_404(Product, product_id=product_id)
    return render(request, 'products/product_detail.html', {'product': product})

# Category CRUD Views
@login_required
def category_list(request):
    categories = Category.objects.all().order_by('name')
    return render(request, 'products/category_list.html', {'categories': categories})

@login_required
def category_create(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description', '')
        
        if name:
            try:
                Category.objects.create(name=name, description=description)
                messages.success(request, f'Category "{name}" created successfully!')
                return redirect('category_list')
            except Exception as e:
                messages.error(request, f'Error creating category: {str(e)}')
        else:
            messages.error(request, 'Category name is required.')
    
    return render(request, 'products/category_form.html', {'action': 'Create'})

@login_required
def category_edit(request, category_id):
    category = get_object_or_404(Category, category_id=category_id)
    
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description', '')
        
        if name:
            try:
                category.name = name
                category.description = description
                category.save()
                messages.success(request, f'Category "{name}" updated successfully!')
                return redirect('category_list')
            except Exception as e:
                messages.error(request, f'Error updating category: {str(e)}')
        else:
            messages.error(request, 'Category name is required.')
    
    return render(request, 'products/category_form.html', {'category': category, 'action': 'Edit'})

@login_required
def category_delete(request, category_id):
    category = get_object_or_404(Category, category_id=category_id)

    if request.method == 'POST':
        category_name = category.name
        try:
            category.delete()
            messages.success(request, f'Category "{category_name}" deleted successfully!')
        except Exception as e:
            messages.error(request, f'Error deleting category: {str(e)}')
        return redirect('category_list')

    return render(request, 'products/category_confirm_delete.html', {'category': category})

# Product CRUD Views
@login_required
def product_create(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description', '')
        price = request.POST.get('price')
        category_id = request.POST.get('category')
        stock_quantity = request.POST.get('stock_quantity')
        image = request.FILES.get('image_url')

        if name and price and category_id and stock_quantity:
            try:
                category = get_object_or_404(Category, category_id=category_id)
                product = Product.objects.create(
                    name=name,
                    description=description,
                    price=price,
                    category=category,
                    stock_quantity=stock_quantity,
                    image_url=image
                )
                messages.success(request, f'Product "{name}" created successfully!')
                return redirect('product_list')
            except Exception as e:
                messages.error(request, f'Error creating product: {str(e)}')
        else:
            messages.error(request, 'All required fields must be filled.')

    categories = Category.objects.all().order_by('name')
    return render(request, 'products/product_form.html', {'categories': categories, 'action': 'Create'})

@login_required
def product_edit(request, product_id):
    product = get_object_or_404(Product, product_id=product_id)

    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description', '')
        price = request.POST.get('price')
        category_id = request.POST.get('category')
        stock_quantity = request.POST.get('stock_quantity')
        image = request.FILES.get('image_url')

        if name and price and category_id and stock_quantity:
            try:
                category = get_object_or_404(Category, category_id=category_id)
                product.name = name
                product.description = description
                product.price = price
                product.category = category
                product.stock_quantity = stock_quantity
                if image:
                    product.image_url = image
                product.save()
                messages.success(request, f'Product "{name}" updated successfully!')
                return redirect('product_list')
            except Exception as e:
                messages.error(request, f'Error updating product: {str(e)}')
        else:
            messages.error(request, 'All required fields must be filled.')

    categories = Category.objects.all().order_by('name')
    return render(request, 'products/product_form.html', {'product': product, 'categories': categories, 'action': 'Edit'})