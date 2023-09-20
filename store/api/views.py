from store.models import Product, Category, ProductTransaction
from rest_framework import permissions, viewsets, status
from django.http import Http404
from rest_framework.views import APIView
from store.api.serializers import ProductSerializers, CategorySerializer, ProductTransactionSerializers
from rest_framework.response import Response


class ProductList(APIView):
    """
    List all products, or create a new product.
    """
    def get(self, request, format=None):
        products = Product.objects.all().order_by('-created')
        serializer = ProductSerializers(products, many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        serializer = ProductSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductDetails(APIView):
    """
    Retrieve, update or delete a product instance.
    """
    def get_object(self, pk):
        try:
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            raise Http404
        
    def get(self, request, pk, format=None):
        product = self.get_object(pk)
        serializer = ProductSerializers(product)
        return Response(serializer.data)
    
    def put(self, request, pk, format=None):
        product = self.get_object(pk)
        serializer = ProductSerializers(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format=None):
        product = self.get_object(pk)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class CategoryList(APIView):
    """
    List all products, or create a new product.
    """
    def get(self, request, format=None):
        category = Category.objects.all()
        serializer = CategorySerializer(category, many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        category = CategorySerializer(data=request.data)
        if category.is_valid():
            category.save()
            return Response(category.data, status=status.HTTP_201_CREATED)
        return Response(category.errors, status=status.HTTP_400_BAD_REQUEST)

class CategoryDetails(APIView):
    """
    Retrieve, update or delete a product instance.
    """
    def get_object(self, pk):
        try:
            return Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            raise Http404
        
    def get(self, request, pk, format=None):
        category = self.get_object(pk)
        serializer = CategorySerializer(category)
        return Response(serializer.data)
    
    def put(self, request, pk, format=None):
        category = self.get_object(pk)
        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format=None):
        category = self.get_object(pk)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProductTransactionList(APIView):
    """
    List all product transactions, or create a new product transaction.
    """
    def get(self, request, format=None):
        transaction = ProductTransaction.objects.all()
        serializer = ProductTransactionSerializers(transaction, many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        transaction = ProductTransactionSerializers(data=request.data)
        if transaction.is_valid():
            transaction.save()
            return Response(transaction.data, status=status.HTTP_201_CREATED)
        return Response(transaction.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductTransactionDetails(APIView):
    """
    Retrieve, update or delete a product transaction instance.
    """
    def get_object(self, pk):
        try:
            return ProductTransaction.objects.get(pk=pk)
        except ProductTransaction.DoesNotExist:
            raise Http404
        
    def get(self, request, pk, format=None):
        transaction = self.get_object(pk)
        serializer = ProductTransactionSerializers(transaction)
        return Response(serializer.data)
    
    def put(self, request, pk, format=None):
        transaction = self.get_object(pk)
        serializer = ProductTransactionSerializers(transaction, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format=None):
        transaction = self.get_object(pk)
        transaction.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# class ProductTransactionViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint that allows product transaction to be viewed or edited.
#     """
#     queryset = ProductTransaction.objects.all()
#     serializer_class = ProductTransactionSerializers
#     permission_classes = [permissions.AllowAny]