from django.urls import path
from . import views

urlpatterns = [
    # Admin order management
    path('admin/', views.admin_orders, name='admin_orders'),
    path('admin/export/', views.admin_orders_export, name='admin_orders_export'),
    path('admin/create/', views.admin_order_create, name='admin_order_create'),
    path('admin/<int:order_id>/', views.admin_order_detail, name='admin_order_detail'),
]
