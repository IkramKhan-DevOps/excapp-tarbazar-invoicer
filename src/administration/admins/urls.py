from django.urls import path
from django.views.generic import TemplateView

from .views import (
    DashboardView,
    ProductListView, ProductCreateView, ProductDeleteView, ProductUpdateView,
    InvoiceListView, InvoiceCreateView, InvoiceDeleteView, InvoiceUpdateView,
    InvoicerView
)

app_name = 'admins'
urlpatterns = [

    path('', DashboardView.as_view(), name='dashboard'),

    path('product/', ProductListView.as_view(), name='product-list'),
    path('product/add/', ProductCreateView.as_view(), name='product-add'),
    path('product/<int:pk>/change/', ProductUpdateView.as_view(), name='product-update'),
    path('product/<int:pk>/delete/', ProductDeleteView.as_view(), name='product-delete'),

    path('invoice/', InvoiceListView.as_view(), name='invoice-list'),
    path('invoice/add/', InvoiceCreateView.as_view(), name='invoice-add'),
    path('invoice/<int:pk>/change/', InvoiceUpdateView.as_view(), name='invoice-update'),
    path('invoice/<int:pk>/delete/', InvoiceDeleteView.as_view(), name='invoice-delete'),

    path('invoicer', InvoicerView.as_view(), name='invoicer')
]
