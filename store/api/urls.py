from django.urls import path, include
# from rest_framework import routers
from store.api.views import ProductList, ProductDetails, CategoryList, CategoryDetails, ProductTransactionList, ProductTransactionDetails
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('products/', ProductList.as_view()),
    path('products/<int:pk>', ProductDetails.as_view()),
    path('categories/', CategoryList.as_view()),
    path('categories/<int:pk>', CategoryDetails.as_view()),
    path('product-transactions/', ProductTransactionList.as_view()),
    path('product-transactions/<int:pk>', ProductTransactionDetails.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)