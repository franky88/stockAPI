from store.models import Product, Category, ProductTransaction
from rest_framework import permissions, viewsets
from store.api.serializers import ProductSerializers, CategorySerializer, ProductTransactionSerializers


class ProductViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows products to be viewed or edited.
    """
    queryset = Product.objects.all().order_by('-created')
    serializer_class = ProductSerializers
    permission_classes = [permissions.AllowAny]

class CategoryViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows category to be viewed or edited.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]

class ProductTransactionViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows product transaction to be viewed or edited.
    """
    queryset = ProductTransaction.objects.all()
    serializer_class = ProductTransactionSerializers
    permission_classes = [permissions.AllowAny]