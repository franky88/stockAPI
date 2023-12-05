from rest_framework import serializers
from store.models import Product, Category, ProductTransaction, OrderTransaction, Supplier, PettyCash
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # fields = '__all__'
        fields = ['id', 'username', 'email', 'groups']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class ProductSerializers(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'id',
            'user',
            'bar_code',
            'name',
            'category',
            'supplier',
            'cost',
            'price',
            'quantity',
            'image',
            'on_display',
            'created',
            'total_cost',
            'with_serial'
        ]

class ProductTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductTransaction
        fields = [
            'id',
            'user',
            'product',
            'cost',
            'quantity',
            'supplier',
        ]

class OrderTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderTransaction
        fields = [
            'id',
            'order_id',
            'customer',
            'product',
            'price',
            'quantity',
            'serials',
            'total_cost',
            'is_accepted',
            'is_paid',
            'remarks',
            'created',
            'is_recent_orders'
        ]

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'get_short_name', 'email', 'last_login', 'date_joined']

class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = ['name', 'address', 'contact', 'is_active']

class PettyCashSerializer(serializers.ModelSerializer):
    class Meta:
        model = PettyCash
        fields = ['request_by', 'purpose', 'amount', 'is_approved']