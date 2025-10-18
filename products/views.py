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