from django.urls import path
from . import views

urlpatterns = [
    path('submit/<int:product_id>/', views.submit_review, name='submit_review'),
    path('view/<int:product_id>/', views.view_reviews, name='view_reviews'),
]