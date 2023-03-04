from django.urls import path, include
from django.views.generic import TemplateView

from .views import (
    DashboardView,
    ProductListView, ProductCreateView, ProductDeleteView, ProductUpdateView,
    InvoiceListView, InvoiceCreateView, InvoiceDeleteView, InvoiceUpdateView,
    InvoicerView, InvoiceDetailView, CompanyUpdateView
)

app_name = 'admins'
urlpatterns = [

    path('', DashboardView.as_view(), name='dashboard'),
    path('company/change/', CompanyUpdateView.as_view(), name='company-update'),

    path('product/', ProductListView.as_view(), name='product-list'),
    path('product/add/', ProductCreateView.as_view(), name='product-add'),
    path('product/<int:pk>/change/', ProductUpdateView.as_view(), name='product-update'),
    path('product/<int:pk>/delete/', ProductDeleteView.as_view(), name='product-delete'),

    path('invoice/', InvoiceListView.as_view(), name='invoice-list'),
    path('invoice/add/', InvoiceCreateView.as_view(), name='invoice-add'),
    path('invoice/<int:pk>/', InvoiceDetailView.as_view(), name='invoice-detail'),
    path('invoice/<int:pk>/change/', InvoiceUpdateView.as_view(), name='invoice-update'),
    path('invoice/<int:pk>/delete/', InvoiceDeleteView.as_view(), name='invoice-delete'),

    path('invoicer', InvoicerView.as_view(), name='invoicer')
]

urlpatterns += [
    path('api/', include('src.administration.admins.api.urls'), name='api-product-list'),
]
