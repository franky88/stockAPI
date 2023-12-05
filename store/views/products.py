from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from store.models import Product
from django.views import View
from store.forms.product import ProductForm


class ProductView(View):
    template_name = "products/product_list.html"
    form_class = ProductForm
    def get(self, request):
        products = Product.objects.all()
        form = self.form_class(request.POST or None)
        context = {
            "title": "Products",
            "products": products,
            "form": form
        }
        return render(request, self.template_name, context)
    
    def post(self, request):
        form = self.form_class(request.POST or None)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            return redirect("store:products_list")
        
class ProductDetailView(View):
    template_name = "products/product_details.html"
    form_class = ProductForm
    def get(self, request, *args, **kwargs):
        porduct_code = kwargs.get('bar_code')
        instance = get_object_or_404(Product, bar_code=porduct_code)
        form = self.form_class(request.POST or None, instance=instance)
        
        context = {
            "title": "product details",
            "instance": instance,
            "form": form
        }
        return render(request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):
        porduct_code = kwargs.get('bar_code')
        instance = get_object_or_404(Product, bar_code=porduct_code)
        form = self.form_class(request.POST or None, instance=instance)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            return redirect("store:products_details", instance.bar_code)
        
class ProductHideUnhideView(View):

    # def get(self, request, *args, **kwargs):
    #     porduct_code = kwargs.get('bar_code')
    #     instance = get_object_or_404(Product, bar_code=porduct_code)
    #     return redirect("store:products_details", instance.bar_code)
    
    def patch(self, request, *args, **kwargs):
        porduct_code = kwargs.get('bar_code')
        instance = get_object_or_404(Product, bar_code=porduct_code)
        if instance.on_display:
            instance.on_display = False
        else:
            instance.on_display = True
        instance.save()
        return redirect("store:products_details", instance.bar_code)

