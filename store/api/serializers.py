from rest_framework import serializers
from store.models import Product, Category, ProductTransaction, OrderTransaction
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
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
            'cost',
            'price',
            'quantity',
            'image',
            'on_display',
            'created',
            'total_cost'
        ]

class ProductTransactionSerializers(serializers.ModelSerializer):
    class Meta:
        model = ProductTransaction
        fields = [
            'id',
            'user',
            'product',
            'cost',
            'quantity'
        ]


class OrderTransactionSerializers(serializers.ModelSerializer):
    class Meta:
        model = OrderTransaction
        fields = [
            'id',
            'customer',
            'product',
            'price',
            'quantity',
            'total_cost',
            'is_recent_orders'
        ]