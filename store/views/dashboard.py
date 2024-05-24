from django.shortcuts import render, redirect
from django.views import View
from store.models import Product, Customer, Repair, OrderTransaction
from django.utils import timezone
from store.cartitems import Cart
import datetime

class DashboardView(View):
    """
    Dashboard view
    """
    template_name = 'dashboard/dashboard.html'
    def get(self, request):
        cart = Cart(self.request)
        items_in_cart = cart.get_cart_data()
        items = items_in_cart['items']
        total_products = Product.objects.all().count()
        total_display_products = Product.objects.filter(on_display=True).count()
        total_hidden_products = Product.objects.filter(on_display=False).count()
        total_customers = Customer.objects.all().count()
        recent_customers = Customer.objects.filter(is_added_recently=True).count()
        active_customers = Customer.objects.filter(is_active=True).count()
        total_repairs = Repair.objects.all().count()
        on_going_repairs = Repair.objects.filter(status__name="on going").count()
        pending_repairs = Repair.objects.filter(status__name="pending").count()
        repaired_repairs = Repair.objects.filter(status__name="repaired").count()
        orders = OrderTransaction.objects.all()
        context = {
            "title": "Dashboard",
            "total_products": total_products,
            "total_customers": total_customers,
            "total_hidden_products": total_hidden_products,
            "total_display_products": total_display_products,
            "total_repairs": total_repairs,
            "recent_customers": recent_customers,
            "active_customers": active_customers,
            "on_going_repairs": on_going_repairs,
            "pending_repairs": pending_repairs,
            "repaired_repairs": repaired_repairs,
            "orders": orders,
            "items_in_cart": items_in_cart,
            "items": items
        }
        return render(request, self.template_name, context)