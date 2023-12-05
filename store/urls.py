from django.urls import path
from store.views.dashboard import DashboardView
from store.views.products import ProductView, ProductDetailView, ProductHideUnhideView

app_name = 'store'
urlpatterns = [
    path('', DashboardView.as_view(), name="dashboard"),
    path('products/', ProductView.as_view(), name="products_list"),
    path('products/<bar_code>/', ProductDetailView.as_view(), name="products_details"),
    path('products/<bar_code>/update/', ProductHideUnhideView.as_view(), name="update_product"),
]