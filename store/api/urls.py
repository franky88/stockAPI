from django.urls import path, include
from rest_framework import routers
from store.api.views import (
                            UserViewSets,
                            ProductViewSets,
                            CategoryViewSets,
                            ProductTransactionViewSets,
                            OrderTransactionViewSets,
                            ProductOrderViewSets,
                            SupplierViewSets,
                            PettyCashViewSets,
                            getRoutes,
                            MyTokenObtainPairView
                             )
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView
)

router = routers.DefaultRouter()

router.register(r'users', UserViewSets, basename="user")
router.register(r'categories', CategoryViewSets, basename="categories")
router.register(r'product-transactions', ProductTransactionViewSets, basename="transactions")
router.register(r'cart', ProductOrderViewSets, basename="cart")
router.register(r'products', ProductViewSets, basename="products")
router.register(r'orders', OrderTransactionViewSets, basename="orders")
router.register(r'suppliers', SupplierViewSets, basename="supplier")
router.register(r'petty-cash', PettyCashViewSets, basename="petty-cash")

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', getRoutes),
    path('auth/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]