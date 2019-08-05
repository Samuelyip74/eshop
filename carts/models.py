from decimal import Decimal
from django.conf import settings
from django.db import models
from products.models import Product
from django.db.models.signals import pre_save, m2m_changed


User = settings.AUTH_USER_MODEL

class CartManager(models.Manager):
    def new_or_get(self, request):
        cart_id = request.session.get("cart_id", None)
        qs = self.get_queryset().filter(id=cart_id)
        if qs.count() == 1:
            new_obj = False
            cart_obj = qs.first()
            if request.user.is_authenticated and cart_obj.user is None:
                cart_obj.user = request.user
                cart_obj.save()
        else:
            cart_obj = Cart.objects.new(user=request.user)
            new_obj = True
            request.session['cart_id'] = cart_obj.id
            request.session['cart_items'] = 0
        return cart_obj, new_obj

    def new(self, user=None):
        user_obj = None
        if user is not None:
            if user.is_authenticated:
                user_obj = user
        return self.model.objects.create(user=user_obj)

class CartItemManager(models.Manager):
    def new_or_get(self, request):
        cart_id = request.session.get("cart_id", None)
        if request.POST.get('product_id') is not None:
            product_id = request.POST.get('product_id')
        elif request.GET.get('product_id') is not None:
            product_id = request.GET.get('product_id')
        print(product_id)
        product_instance = Product.objects.get(id=product_id)
        print(product_instance.title)
        qs = self.get_queryset().filter(cartid=cart_id)
        if qs.count() == 1:
            new_obj = False
            cartitem_obj = qs.first()
        else:
            cartitem_obj = CartItem.objects.new(cartid=cart_id)
            product_instance = Product.objects.get(id=product_id)
            print(product_instance.title)
            cartitem_obj.item = product_instance.title
            cartitem_obj.save()
            new_obj = True
            # request.session['cart_id'] = cart_obj.id
        return cartitem_obj, new_obj

    def new(self, cartid=None):
        cartid_obj = None
        if cartid is not None:
            cartid_obj = cartid
        return self.model.objects.create(cartid=cartid_obj)        

class CartItem(models.Model):
    item        = models.ForeignKey(Product,null=True, blank=True,on_delete='CASCADE')
    quantity    = models.IntegerField(default=1,null=True, blank=True)
    cartid      = models.IntegerField(null=True, blank=True) 

    objects = CartItemManager()

    def __str__(self):
        return f"{self.quantity} unit(s) of {self.item.title} in Cart {self.cartid}"

    def get_total_item_price(self):
        return self.quantity * self.item.price

    def get_final_price(self):
        # if self.item.discount_price:
        #     return self.get_total_discount_item_price()
        return self.get_total_item_price()        


class Cart(models.Model):
    user        = models.ForeignKey(User, null=True, blank=True, on_delete='CASCADE')
    items        = models.ManyToManyField(CartItem,blank=True)
    products    = models.ManyToManyField(Product, blank=True)
    subtotal    = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
    total       = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
    updated     = models.DateTimeField(auto_now=True)
    timestamp   = models.DateTimeField(auto_now_add=True)

    objects = CartManager()

    def __str__(self):
         return str(self.id)

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        print(total)
        # if self.coupon:
        #     total -= self.coupon.amount
        return total           

    # @property
    # def is_digital(self):
    #     qs = self.products.all() #every product
    #     new_qs = qs.filter(is_digital=False) # every product that is not digial
    #     if new_qs.exists():
    #         return False
    #     return True

def m2m_changed_cart_receiver(sender, instance, action, *args, **kwargs):
    if action == 'post_add' or action == 'post_remove' or action == 'post_clear':
        products = instance.products.all()
        total = 0
        for x in products:
            total += x.price
        if instance.subtotal != total:
            instance.subtotal = total
            instance.save()

m2m_changed.connect(m2m_changed_cart_receiver, sender=Cart.products.through)

def pre_save_cart_receiver(sender, instance, *args, **kwargs):
    if instance.subtotal > 0:
        instance.total = Decimal(instance.subtotal) * Decimal(1.08) # 8% tax
    else:
        instance.total = 0.00

pre_save.connect(pre_save_cart_receiver, sender=Cart)