import django_filters
from django.forms import TextInput

from src.accounts.models import User
from src.administration.admins.models import Product


class UserFilter(django_filters.FilterSet):
    username = django_filters.CharFilter(widget=TextInput(attrs={'placeholder': 'username'}), lookup_expr='icontains')
    first_name = django_filters.CharFilter(widget=TextInput(attrs={'placeholder': 'first name'}), lookup_expr='icontains')
    last_name = django_filters.CharFilter(widget=TextInput(attrs={'placeholder': 'last name'}), lookup_expr='icontains')
    email = django_filters.CharFilter(widget=TextInput(attrs={'placeholder': 'email'}), lookup_expr='icontains')

    class Meta:
        model = User
        fields = {}


class ProductFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(widget=TextInput(attrs={'placeholder': 'Product Name'}), lookup_expr='icontains')
    code = django_filters.CharFilter(widget=TextInput(attrs={'placeholder': 'Product Code'}), lookup_expr='icontains')

    class Meta:
        model = Product
        fields = [
            'is_active'
        ]