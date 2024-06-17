from rest_framework import serializers
from store.models import Product, Category, ProductTransaction, OrderTransaction, Supplier, PettyCash
from django.contrib.auth.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        return token

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

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['category'] = instance.category.name
        data['user'] = instance.user.username
        if instance.image:
            data['image'] = 'http://localhost:8000'+instance.image.image.url
        else:
            data['image'] = instance.image
        return data

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
        fields = ['id','first_name', 'last_name', 'get_short_name', 'email', 'last_login', 'date_joined']

class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = ['name', 'address', 'contact', 'is_active']

class PettyCashSerializer(serializers.ModelSerializer):
    class Meta:
        model = PettyCash
        fields = ['request_by', 'purpose', 'amount', 'is_approved']