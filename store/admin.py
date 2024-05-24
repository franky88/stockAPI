from django.contrib import admin
from store.models import Product, Category, Customer, Repair, RepairStatus, RepairType, Image

# Register your models here.
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Customer)
admin.site.register(Repair)
admin.site.register(RepairStatus)
admin.site.register(RepairType)
admin.site.register(Image)
