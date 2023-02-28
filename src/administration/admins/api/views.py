from rest_framework import generics
from rest_framework.filters import SearchFilter

from src.administration.admins.api.serializers import ProductSerializer, InvoiceSerializer
from src.administration.admins.models import Product, Invoice


class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [SearchFilter]
    filterset_fields = ['id', 'name', 'code']


class InvoiceCreateView(generics.CreateAPIView):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer


