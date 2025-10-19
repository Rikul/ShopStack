from django.contrib import admin

from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1


class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]
    list_display = ('order_id', 'customer', 'total_amount', 'status', 'created_at')
    search_fields = ('customer__username', 'status')


admin.site.register(Order, OrderAdmin)
