from django.contrib import admin
from .models import Sale

@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ('product', 'worker', 'quantity', 'unit_price', 'total_price', 'sold_at')
    list_filter = ('sold_at', 'worker')
    search_fields = ('product__name', 'worker__email')
    date_hierarchy = 'sold_at'
