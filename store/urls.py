from django.urls import path
from store.views.dashboard import DashboardView
from store.views.products import ProductView, ProductDetailView, ProductHideUnhideView, ProductAddToCartView

app_name = 'store'
urlpatterns = [
    path('', DashboardView.as_view(), name="dashboard"),
    path('products/', ProductView.as_view(), name="products_list"),
    path('products/<bar_code>/', ProductDetailView.as_view(), name="products_details"),
    path('products/<bar_code>/hide_unhide/', ProductHideUnhideView.as_view(), name="update_product"),
    path('products/<bar_code>/add_to_cart/', ProductAddToCartView.as_view(), name="add_to_cart"),
]