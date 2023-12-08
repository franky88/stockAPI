from store.models import Product, Category, ProductTransaction, OrderTransaction, Supplier, PettyCash
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action, api_view
from store.api.serializers import (
    ProductSerializers,
    CategorySerializer,
    ProductTransactionSerializer,
    OrderTransactionSerializer,
    UserSerializer,
    SupplierSerializer,
    PettyCashSerializer,
    MyTokenObtainPairSerializer
    )
from rest_framework.response import Response
from store.cartitems import Cart
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from rest_framework_simplejwt.views import TokenObtainPairView



@api_view(['GET'])
def getRoutes(request):
    routes = [
        "/token",
        "/token/refresh"
    ]
    return Response(routes)

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

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
    # permission_classes = [IsAuthenticated]

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
    def with_serial(self, request):
        products = Product.objects.filter(with_serial=True)
        page = self.paginate_queryset(products)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)
    
    @action(detail=False)
    def hidden_products(self, request):
        products = Product.objects.filter(on_display=False)
        page = self.paginate_queryset(products)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['GET','PUT'])
    def hide_product(self, request, *args, **kwargs):
        product = self.get_object()
        if product:
            product.on_display = False
            product.save()
            serializer = self.serializer_class(product)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
        
    @action(detail=True, methods=['GET','PUT'])
    def unhide_product(self, request, *args, **kwargs):
        product = self.get_object()
        if product:
            product.on_display = True
            product.save()
            serializer = self.serializer_class(product)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=True, methods=['GET','POST'])
    def add_product_order(self, request, *args, **kwargs):
        product = self.get_object()
        cart = Cart(self.request)
        if product.on_display and product.quantity >= 0:
            cart.add(product=product, quantity=1, update_quantity=False)
            cart_data = cart.get_cart_data()
            return Response(cart_data, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Please check product is on display or check the product quantity"}, status=status.HTTP_400_BAD_REQUEST)

class CategoryViewSets(viewsets.ModelViewSet):
    """
    List all products, or create a new product.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    # permission_classes = [IsAuthenticated]

class ProductTransactionViewSets(viewsets.ModelViewSet):
    """
    List all product transactions, or create a new product transaction.
    """
    queryset = ProductTransaction.objects.all()
    serializer_class = ProductTransactionSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        transaction = ProductTransactionSerializer(data=request.data)
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
    serializer_class = OrderTransactionSerializer
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
            serializer = OrderTransactionSerializer(obj)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Missing 'is_accepted' in request data"}, status=status.HTTP_400_BAD_REQUEST)
        
    @action(detail=True, methods=['GET','PUT'])
    def unaccept_order(self, request, *args, **kwargs):
        obj = self.get_object()
        print(obj)
        if obj is not None:
            if obj.is_accepted:
                obj.is_accepted = False
                obj.save()
                serializer = OrderTransactionSerializer(obj)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({"message": "Order aleady unaccepted!"}, status=status.HTTP_202_ACCEPTED)
        else:
            return Response({"detail": "Missing 'is_accepted' in request data"}, status=status.HTTP_400_BAD_REQUEST)
        
class ProductOrderViewSets(viewsets.ViewSet):
    """
    List all product in cart, update and delete items in the cart.
    """
    permission_classes = [IsAuthenticated]
    def list(self, request):
        cart = Cart(self.request)
        queryset = cart.get_cart_data()
        return Response(queryset, status=status.HTTP_200_OK)

    @action(detail=False, methods=['GET'])
    def get_cart_data(self, request):
        cart = Cart(self.request)
        items = cart.get_cart_data()
        if items:
            return Response(items, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'No items in the cart'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['DELETE'])
    def clear_cart_items(self, request, format=None):
        cart = Cart(self.request)
        items = cart.clear()
        if items:
            return Response(items, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'No items in the cart'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['DELETE'])
    def delete_cart_item(self, request, pk=None, format=None):
        instance = get_object_or_404(Product, pk=pk)
        cart = Cart(self.request)
        item = cart.remove(product=instance)
        if item:
            return Response(item, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'No items in the cart'}, status=status.HTTP_404_NOT_FOUND)
        
    @action(detail=False, methods=['POST'])
    def process_order(self, request, format=None):
        cart = Cart(self.request)
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
        return Response(status=status.HTTP_200_OK)
    
class SupplierViewSets(viewsets.ModelViewSet):
    """
    List all supplier, or create a new supplier.
    """
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    permission_classes = [IsAuthenticated]

class PettyCashViewSets(viewsets.ModelViewSet):
    """
    List all petty cash, or create a new supplier.
    """
    queryset = PettyCash.objects.all()
    serializer_class = PettyCashSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False)
    def approved_petty(self, request):
        petty = PettyCash.objects.filter(is_approved=True)
        page = self.paginate_queryset(petty)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(petty, many=True)
        return Response(serializer.data)
    
    @action(detail=False)
    def unapproved_petty(self, request):
        petty = PettyCash.objects.filter(is_approved=False)
        page = self.paginate_queryset(petty)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(petty, many=True)
        return Response(serializer.data)