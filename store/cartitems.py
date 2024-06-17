from decimal import Decimal
from django.conf import settings

from .models import Product


class Cart(object):
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product, quantity=1, update_quantity=False):
        product_id = str(product.id)
        if product.quantity > 0:
            if product_id not in self.cart:
                self.cart[product_id] = {'quantity': 0, 'price': str(product.price)}
            if update_quantity:
                self.cart[product_id]['quantity'] = quantity
            else:
                self.cart[product_id]['quantity'] += quantity
        self.save()

    def get_cart_data(self):
        # Return cart data as a dictionary
        cart_data = {
            'items': {},
            'total_quantity': 0,
            'total_price': 0,
        }

        for product_id, item_data in self.cart.items():
            product = Product.objects.get(id=product_id)
            quantity = item_data['quantity']
            price = Decimal(item_data['price'])
            subtotal = quantity * price
            image = ""
            if product.image.image.url == "":
                image = ""
            else:
                image = product.image.image.url

            print(image)

            cart_data['items'][product_id] = {
                'product_id': product_id,
                'name': product.name,
                'quantity': quantity,
                'image': image,
                'price': str(price),
                'subtotal': str(subtotal),
            }

            cart_data['total_quantity'] += quantity
            cart_data['total_price'] += subtotal

        return cart_data

    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        for product in products:
            self.cart[str(product.id)]['product'] = product

        for item in self.cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True