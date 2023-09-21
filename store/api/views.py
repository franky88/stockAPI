from store.models import Product, Category, ProductTransaction, OrderTransaction
from rest_framework import permissions, viewsets, status
from django.http import Http404, HttpResponse, JsonResponse
from rest_framework.views import APIView
from store.api.serializers import ProductSerializers, CategorySerializer, ProductTransactionSerializers, OrderTransactionSerializers
from rest_framework.response import Response
from store.cartitems import Cart
from django.core import serializers
from django.shortcuts import get_object_or_404


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
            instance = transaction.save()
            instance.user = request.user
            instance.product.quantity += instance.quantity
            if instance.cost:
                instance.product.cost = instance.new_cost
            else:
                instance.cost = instance.product.cost
            instance.product.save()
            instance.save()
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
        if transaction.product.quantity < transaction.quantity:
            return HttpResponse({"quantity is out of range"})
        transaction.product.quantity -= transaction.quantity
        transaction.product.save()
        transaction.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class OrderTransactionSerializersList(APIView):
    """
    List all product transactions, or create a new product transaction.
    """
    def get(self, request, format=None):
        transaction = OrderTransaction.objects.all()
        serializer = OrderTransactionSerializers(transaction, many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        transaction = OrderTransactionSerializers(data=request.data)
        if transaction.is_valid():
            transaction.save()
            return Response(transaction.data, status=status.HTTP_201_CREATED)
        return Response(transaction.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductOrderList(APIView):
    """
    List all product in cart.
    """
    def get(self, request, format=None):
        cart = Cart(request)
        cart_data = cart.get_cart_data()
        return Response(cart_data)
    
class AddProductOrder(APIView):
    """
    Add product in cart
    """
    def get(self, request, pk, format=None):
        cart = Cart(request)
        product = get_object_or_404(Product, pk=pk)
        if product:
            cart.add(product=product, quantity=1, update_quantity=False)
            cart_data = cart.get_cart_data()
            return Response(cart_data)
        else:
            return Response(status.HTTP_404_NOT_FOUND)
        
class MinusProductOrder(APIView):
    """
    Add product quantity
    """
    def get(self, request, pk, format=None):
        cart = Cart(request)
        product = get_object_or_404(Product, pk=pk)
        if product:
            cart.minus(product=product, quantity=1, update_quantity=False)
            cart_data = cart.get_cart_data()
            return Response(cart_data)
        else:
            return Response(status.HTTP_404_NOT_FOUND)
    
class ClearCartList(APIView):
    def get(self, request):
        cart = Cart(request)
        if cart:
            cart.clear()
            return Response(status.HTTP_200_OK)
        else:
            return Response(status.HTTP_200_OK)
        

class ProcessOrderItems(APIView):
    def get(self, request):
        cart = Cart(request)
        cart_data = cart.get_cart_data()
        return Response(cart_data)
    
    def post(self, request):
        cart = Cart(request)
        for item in cart:
            order = OrderTransaction(
                customer = request.user,
                product = item['product'],
                price = item['price'],
                quantity = item['quantity']
            )
            order.product.quantity -= order.quantity
            order.product.save()
            order.save()
        cart.clear()
        return Response(status.HTTP_202_ACCEPTED)