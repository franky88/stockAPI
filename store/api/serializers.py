from rest_framework import serializers
from store.models import Product, Category, ProductTransaction
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['url', 'name']


class ProductSerializers(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'url',
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
        ]

class ProductTransactionSerializers(serializers.ModelSerializer):
    class Meta:
        model = ProductTransaction
        fields = [
            'url',
            'user',
            'product',
            'cost',
            'quantity',
        ]