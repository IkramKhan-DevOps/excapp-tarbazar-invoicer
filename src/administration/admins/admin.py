from django.contrib import admin
from .models import (
    Product, InvoiceItem, Invoice
)


class ProductAdmin(admin.ModelAdmin):
    list_filter = ['is_active']
    list_display = ['id', 'name', 'code', 'rate', 'vat', 'is_active', 'created_on']


class InvoiceAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer_name', 'total', 'vat', 'grand_total', 'is_active', 'created_on']


class InvoiceItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'invoice', 'quantity', 'amount', 'vat']


admin.site.register(Product, ProductAdmin)
admin.site.register(Invoice, InvoiceAdmin)
admin.site.register(InvoiceItem, InvoiceItemAdmin)
