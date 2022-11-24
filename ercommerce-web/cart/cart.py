from django.conf import settings

from product.models import Product


class Cart(object):
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)

        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def __iter__(self):
        # because item has length, "product" mean we get the items
        for p in self.cart.keys():
            # str the id,
            self.cart[str(p)]["product"] = Product.objects.get(pk=p)
        for item in self.cart.values():
            item["total_price"] = item["product"].price * item["quantity"]
            # e.g, values se la {"quantity": x, "id": x, "total_price": x}

            yield item

    def __len__(self):
        return sum(item["quantity"] for item in self.cart.values())

    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modifed = True

    def add(self, product_id, quantity=1, update_quantity=False):
        # cai nay la se 1 cai dictionary kieu {'5': {'quantity': 2, 'id': '5', 'product': object Product trong product/models.py}}

        product_id = str(product_id)
        if update_quantity:
            self.cart[product_id]["quantity"] += int(quantity)
        else:
            if product_id not in self.cart:
                self.cart[product_id] = {"quantity": 1, "id": product_id}
            else:
                self.cart[product_id]["quantity"] += 1
        if self.cart[product_id]["quantity"] == 0:
            print("bang 0 thi xoa")
            self.remove(product_id)

        print(self.cart)
        self.save()

    def remove(self, product_id):
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def get_total_cost(self):
        for p in self.cart.keys():
            # str the id,
            self.cart[str(p)]["product"] = Product.objects.get(pk=p)
        total = int(sum(item["product"].price * item["quantity"]
                        for item in self.cart.values()))
        return f"{total:,.2f}"

    def get_item(self, product_id):
        if str(product_id) in self.cart:
            return self.cart[str(product_id)]
        else:
            return None

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True
