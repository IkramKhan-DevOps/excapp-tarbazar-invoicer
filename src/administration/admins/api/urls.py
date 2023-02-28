from django.urls import path
from rest_framework.routers import DefaultRouter

from src.administration.admins.api.views import ProductListView, InvoiceCreateView

app_name = 'api'
router = DefaultRouter()
urlpatterns = router.urls

urlpatterns += [
    path('product/', ProductListView.as_view(), name='product-list'),
    path('invoice/add/', InvoiceCreateView.as_view(), name='invoice-add'),
]