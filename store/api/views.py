from store.models import Product, Category, ProductTransaction, OrderTransaction
from rest_framework import permissions, viewsets, status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from store.api.serializers import ProductSerializers, CategorySerializer, ProductTransactionSerializers, OrderTransactionSerializers, UserSerializer
from rest_framework.response import Response
from store.cartitems import Cart
from django.core import serializers
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User


class UserViewSets(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

class ProductViewSets(viewsets.ModelViewSet):
    """
    List all products, or create a new product.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializers
    permission_classes = [IsAuthenticated]

    @action(detail=False)
    def recent_products(self, request):
        recent_products = Product.objects.all().order_by('-created')
        page = self.paginate_queryset(recent_products)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(recent_products, many=True)
        return Response(serializer.data)
    
    @action(detail=False)
    def out_of_stock(self, request):
        products = Product.objects.filter(quantity=0)
        page = self.paginate_queryset(products)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)
    
    @action(detail=False)
    def unpublished_products(self, request):
        products = Product.objects.filter(on_display=False)
        page = self.paginate_queryset(products)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)

class CategoryViewSets(viewsets.ModelViewSet):
    """
    List all products, or create a new product.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

class ProductTransactionViewSets(viewsets.ModelViewSet):
    """
    List all product transactions, or create a new product transaction.
    """
    queryset = ProductTransaction.objects.all()
    serializer_class = ProductTransactionSerializers
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
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
            return super().create(request, *args, **kwargs)
        else:
            return Response(transaction.errors, status=status.HTTP_400_BAD_REQUEST)
    
class OrderTransactionViewSets(viewsets.ModelViewSet):
    """
    List all order transactions, or create a new order transaction.
    """
    queryset = OrderTransaction.objects.all()
    serializer_class = OrderTransactionSerializers
    permission_classes = [IsAuthenticated]

    @action(detail=False)
    def unpaid_orders(self, request):
        orders = OrderTransaction.objects.filter(is_paid=False)
        page = self.paginate_queryset(orders)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(orders, many=True)
        return Response(serializer.data)
    
    @action(detail=False)
    def paid_orders(self, request):
        orders = OrderTransaction.objects.filter(is_paid=True)
        page = self.paginate_queryset(orders)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(orders, many=True)
        return Response(serializer.data)
    
    @action(detail=False)
    def unaccepted_orders(self, request):
        orders = OrderTransaction.objects.filter(is_accepted=False)
        page = self.paginate_queryset(orders)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(orders, many=True)
        return Response(serializer.data)
    
    @action(detail=False)
    def accepted_orders(self, request):
        orders = OrderTransaction.objects.filter(is_accepted=True)
        page = self.paginate_queryset(orders)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(orders, many=True)
        return Response(serializer.data)
    
    @action(detail=False)
    def recent_orders(self, request):
        orders = OrderTransaction.objects.all().order_by('-created')
        page = self.paginate_queryset(orders)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(orders, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['GET','PUT'])
    def accept_order(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj is not None:
            if obj.is_accepted:
                return Response({"message": "Order aleady accepted!"}, status=status.HTTP_202_ACCEPTED)
            else:
                obj.is_accepted = True
                obj.save()
            serializer = OrderTransactionSerializers(obj)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Missing 'is_accepted' in request data"}, status=status.HTTP_400_BAD_REQUEST)
        
    @action(detail=True, methods=['GET','PUT'])
    def unaccept_order(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj is not None:
            if obj.is_accepted:
                obj.is_accepted = False
                obj.save()
                serializer = OrderTransactionSerializers(obj)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({"message": "Order aleady unaccepted!"}, status=status.HTTP_202_ACCEPTED)
        else:
            return Response({"detail": "Missing 'is_accepted' in request data"}, status=status.HTTP_400_BAD_REQUEST)


class ProductOrderViewSets(viewsets.ModelViewSet):
    """
    List all product in cart.
    """
    # queryset = OrderTransaction.objects.all()
    # serializer_class = OrderTransactionSerializers
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        cart = Cart(request)
        cart_data = cart.get_cart_data()
        return Response(cart_data)

    # def get(self, request, format=None):
    #     cart = Cart(request)
    #     cart_data = cart.get_cart_data()
    #     return Response(cart_data)
    
# class AddProductOrder(APIView):
#     """
#     Add product in cart
#     """
#     def get(self, request, pk, format=None):
#         cart = Cart(request)
#         product = get_object_or_404(Product, pk=pk)
#         if product:
#             cart.add(product=product, quantity=1, update_quantity=False)
#             cart_data = cart.get_cart_data()
#             return Response(cart_data)
#         else:
#             return Response(status.HTTP_404_NOT_FOUND)
        
# class MinusProductOrder(APIView):
#     """
#     Add product quantity
#     """
#     def get(self, request, pk, format=None):
#         cart = Cart(request)
#         product = get_object_or_404(Product, pk=pk)
#         if product:
#             cart.minus(product=product, quantity=1, update_quantity=False)
#             cart_data = cart.get_cart_data()
#             return Response(cart_data)
#         else:
#             return Response(status.HTTP_404_NOT_FOUND)
    
# class ClearCartList(APIView):
#     def get(self, request):
#         cart = Cart(request)
#         if cart:
#             cart.clear()
#             return Response(status.HTTP_200_OK)
#         else:
#             return Response(status.HTTP_200_OK)
        
# class ProcessOrderItems(APIView):
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