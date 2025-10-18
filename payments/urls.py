from django.urls import path
from . import views

urlpatterns = [
    # Admin payment management
    path('admin/', views.admin_payments, name='admin_payments'),
    path('admin/<int:payment_id>/', views.admin_payment_detail, name='admin_payment_detail'),
    
    # Payment processing
    path('process/<int:order_id>/', views.process_payment, name='process_payment'),
]