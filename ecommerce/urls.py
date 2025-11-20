from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.conf import settings
from django.conf.urls.static import static
from dashboard import views as dashboard_views

def redirect_to_dashboard(request):
    return redirect('dashboard:dashboard')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', redirect_to_dashboard, name='home'),
    path('dashboard/', include('dashboard.urls')),
    path('inventory/', dashboard_views.inventory_view, name='inventory'),
    path('accounts/', include('accounts.urls')),
    path('products/', include('products.urls')),
    path('orders/', include('orders.urls')),
    path('payments/', include('payments.urls'))
]

# Serve media files
# NOTE: For production, consider using a web server (Nginx/Apache) or cloud storage (S3/Azure)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)