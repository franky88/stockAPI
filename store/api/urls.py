from django.urls import path, include
from rest_framework import routers
from store.api.views import ProductViewSet, CategoryViewSet, ProductTransactionViewSet

router = routers.DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'products-transactions', ProductTransactionViewSet)


urlpatterns = [
    path('', include(router.urls)),
]