import uuid
import datetime
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from PIL import Image
from io import BytesIO
from django.utils import timezone

# Create your models here.
class TimeStampedModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-updated','-created')

class Category(models.Model):
    name = models.CharField(max_length=120)

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

class Supplier(models.Model):
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=200, blank=True, null=True)
    contact = models.CharField(max_length=100)
    is_active = models.BooleanField(default=False)
    timestamp = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name

def image_directory_path(instance, filename):
    print(filename)
    return 'images_{0}/{1}'.format(instance, filename)

class Image(models.Model):
    image = models.ImageField(upload_to=image_directory_path, blank=True, null=True)

    def __str__(self):
        return self.image.name

class Product(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bar_code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, blank=True, null=True)
    cost = models.FloatField()
    price = models.FloatField()
    quantity = models.IntegerField()
    with_serial = models.BooleanField(default=False)
    warranty_in_months = models.IntegerField(blank=True, null=True)
    image = models.ForeignKey(Image,  on_delete=models.SET_NULL, null=True, blank=True)
    on_display = models.BooleanField(default=True, verbose_name="this product is available?")

    @property
    def total_cost(self):
        total = self.cost * float(self.quantity)
        return total

    def __str__(self):
        return self.name
    

class ProductTransaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cost = models.FloatField(blank=True, null=True)
    quantity = models.PositiveIntegerField(default=1)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created', '-updated']

    @property
    def new_cost(self):
        current_quantity = self.product.quantity
        current_cost = self.product.cost

        new_added_quantity = self.quantity
        new_added_cost = self.cost

        if current_quantity:
            updated_cost = ((current_quantity/(current_quantity + new_added_quantity)) * \
                            current_cost) + ((new_added_quantity/(current_quantity + new_added_quantity)) * new_added_cost)
        else:
            updated_cost = new_added_cost
        return updated_cost

    @property
    def total_cost(self):
        total = self.cost * float(self.quantity)
        return total

    def __str__(self):
        return self.product.name
    
class Customer(models.Model):
    name = models.CharField(max_length=200)
    address = models.TextField(blank=True, null=True)
    contact = models.CharField(max_length=20, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_added_recently = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class OrderTransaction(models.Model):
    order_id = models.CharField(max_length=12, unique=True)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.FloatField()
    quantity = models.PositiveIntegerField()
    serials = models.TextField(blank=True, null=True)
    is_paid = models.BooleanField(default=False)
    is_accepted = models.BooleanField(default=False)
    remarks = models.CharField(max_length=200, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-is_accepted','-created']

    @property
    def total_cost(self):
        cost = self.price * self.quantity
        return cost
    
    @property
    def change(self):
        change = self.total_amount - self.money_tender
        return change
    
    @property
    def balance(self):
        if not self.is_paid:
            balance = self.total_cost
        else:
            balance = 0.0
        return balance
    
    @property
    def is_recent_orders(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.created <= now

    def __str__(self):
        return self.customer.username

class RepairType(models.Model):
    name = models.CharField(max_length=255)
    service_fee = models.FloatField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    
class RepairStatus(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Repair(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    repair_type = models.ForeignKey(RepairType, on_delete=models.SET_NULL, blank=True, null=True)
    product_descriptions = models.TextField()
    problems = models.TextField(blank=True, null=True)
    status = models.ForeignKey(RepairStatus, on_delete=models.SET_NULL, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.customer.name
    
class PettyCash(models.Model):
    request_by = models.ForeignKey(User, on_delete=models.CASCADE)
    purpose = models.CharField(max_length=200)
    amount = models.FloatField()
    is_approved = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.purpose


class ItemRequest(models.Model):
    request_by = models.ForeignKey(User, on_delete=models.CASCADE)
    item_name = models.CharField(max_length=120)
    message = models.CharField(max_length=120, blank=True, null=True)
    is_noted = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.request_by

@receiver(post_save, sender=OrderTransaction)
def order_pro_save(sender, instance, created, *args, **kwargs):
    if created:
        uuid_code = str(uuid.uuid4()).replace("-", "").upper()[:8]
        instance.order_id = uuid_code
        instance.save()

@receiver(post_save, sender=Customer)
def is_added_recently_post_save(sender, instance, created, *args, **kwargs):
    if created:
        now = timezone.now()
        instance.is_added_recently = now - datetime.timedelta(days=1) <= instance.timestamp <= now
    else:
        instance.is_added_recently = False
    instance.save()