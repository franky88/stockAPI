from django.urls import path, include
# from rest_framework import routers
from store.api.views import (ProductList, 
                             ProductDetails,
                             CategoryList,
                             CategoryDetails,
                             ProductTransactionList,
                             ProductTransactionDetails,
                             OrderTransactionSerializersList,
                             ProductOrderList,
                             AddProductOrder,
                             MinusProductOrder,
                             ClearCartList,
                             ProcessOrderItems
                             )
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('products/', ProductList.as_view()),
    path('products/<int:pk>', ProductDetails.as_view()),
    path('products/orders/', ProductOrderList.as_view(), name="order"),
    path('products/orders/clear/', ClearCartList.as_view()),
    path('products/orders/add/<int:pk>', AddProductOrder.as_view(), name="add"),
    path('products/orders/minus/<int:pk>', MinusProductOrder.as_view(), name="minus"),

    path('categories/', CategoryList.as_view()),
    path('categories/<int:pk>', CategoryDetails.as_view()),
    path('product-transactions/', ProductTransactionList.as_view()),
    path('product-transactions/<int:pk>', ProductTransactionDetails.as_view()),
    path('order-transactions/', OrderTransactionSerializersList.as_view()),
    path('order-transactions/<int:pk>', OrderTransactionSerializersList.as_view()),

    path('orders/', ProcessOrderItems.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)