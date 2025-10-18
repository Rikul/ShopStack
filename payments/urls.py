from django.urls import path
from . import views

urlpatterns = [
    # Admin payment management
    path('admin/', views.admin_payments, name='admin_payments'),
    path('admin/export/', views.admin_payments_export, name='admin_payments_export'),
    path('admin/create/', views.admin_payment_create, name='admin_payment_create'),
    path('admin/<int:payment_id>/', views.admin_payment_detail, name='admin_payment_detail'),
]
