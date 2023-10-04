from django.shortcuts import render, redirect
from django.views import View
from store.models import Product, Customer, Repair

class DashboardView(View):
    """
    Dashboard view
    """
    template_name = 'dashboard/dashboard.html'
    def get(self, request):
        total_products = Product.objects.all().count()
        total_display_products = Product.objects.filter(on_display=True).count()
        total_hidden_products = Product.objects.filter(on_display=False).count()
        total_customers = Customer.objects.all().count()
        total_repairs = Repair.objects.all().count()
        context = {
            "title": "Dashboard",
            "total_products": total_products,
            "total_customers": total_customers,
            "total_hidden_products": total_hidden_products,
            "total_display_products": total_display_products,
            "total_repairs": total_repairs,
        }
        return render(request, self.template_name, context)