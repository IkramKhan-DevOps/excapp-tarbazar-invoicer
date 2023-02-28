from django.urls import path
from rest_framework.routers import DefaultRouter

from src.administration.admins.api.views import ProductListView

app_name = 'api'
router = DefaultRouter()
urlpatterns = router.urls

urlpatterns += [
    path('product/', ProductListView.as_view(), name='product-list'),
]