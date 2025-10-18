from django.urls import path
from . import views

urlpatterns = [
    # Admin order management
    path('admin/', views.admin_orders, name='admin_orders'),
    path('admin/<int:order_id>/', views.admin_order_detail, name='admin_order_detail'),
    
    # Customer cart functionality
    path('cart/', views.cart_view, name='cart'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout_view, name='checkout'),
]