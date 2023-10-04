from django.urls import path, include
from rest_framework import routers
from store.api.views import (
                            UserViewSets,
                            ProductViewSets,
                            CategoryViewSets,
                            ProductTransactionViewSets,
                            OrderTransactionViewSets,
                            ProductOrderViewSets,
                            SupplierViewSets
                             )
from rest_framework.urlpatterns import format_suffix_patterns

router = routers.DefaultRouter()

router.register(r'users', UserViewSets, basename="user")
router.register(r'categories', CategoryViewSets, basename="categories")
router.register(r'product-transactions', ProductTransactionViewSets, basename="transactions")
router.register(r'cart', ProductOrderViewSets, basename="cart")
router.register(r'products', ProductViewSets, basename="products")
router.register(r'orders', OrderTransactionViewSets, basename="orders")
router.register(r'suppliers', SupplierViewSets, basename="supplier")

urlpatterns = [
    path('', include(router.urls)),
]