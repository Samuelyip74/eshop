from django.http import JsonResponse
from django.contrib import messages

from django.shortcuts import render,redirect,get_object_or_404

from accounts.forms import LoginForm, GuestForm
from accounts.models import GuestEmail
from orders.models import Order

from addresses.forms import AddressForm
from addresses.models import Address

from products.models import Product
from .models import Cart,CartItem
from billing.models import BillingProfile

def cart_detail_api_view(request):
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    products = [{
            "id": x.id,
            "url": x.get_absolute_url(),
            "name": x.name,
            "description": x.description,
            "price": x.price
            }
            for x in cart_obj.products.all()]
    cart_data  = {"products": products, "subtotal": cart_obj.subtotal, "total": cart_obj.total}
    return JsonResponse(cart_data)

def cart_home(request):
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    return render(request, "carts/home.html", {"cart": cart_obj})

def cart_update(request):
    # Get Product ID from HTTP Request.  
    if request.POST.get('product_id') is not None:
        product_id = request.POST.get('product_id')
    elif request.GET.get('product_id') is not None:
        product_id = request.GET.get('product_id')

    if product_id is not None:
        try:
            # Check if Product is still available in Database.  
            product_obj = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            print("Show message to user, product is gone?")
            return redirect("cart:home")
        
        # Check if there is an existing shopping cart id, else create one.  
        cart_obj, new_obj = Cart.objects.new_or_get(request)

        if new_obj is True:
            print(new_obj)
            request.session['cart_items'] = 0

        # Add the item to cart if not exist.  If exist, get itemInCart object  
        itemInCart, new_item = CartItem.objects.get_or_create(
                item=product_obj,
                cartid=cart_obj.id,
        )

        # If item already in cart, increment quantity
        if new_item is False:
            itemInCart.quantity +=1
            itemInCart.save()
            cart_obj.items.add(itemInCart)
            request.session['cart_items'] += 1

        else:
            cart_obj.items.add(itemInCart)
            request.session['cart_items'] += 1

        if product_obj in cart_obj.products.all():
            # cart_obj.products.remove(product_obj)
            added = False
        else:
            # cart_obj.products.add(product_obj) # cart_obj.products.add(product_id)
            added = True
        # request.session['cart_items'] = cart_obj.products.count()

        # return redirect(product_obj.get_absolute_url())
        if request.is_ajax(): # Asynchronous JavaScript And XML / JSON
            print("Ajax request")
            json_data = {
                "added": added,
                "removed": not added,
                "cartItemCount": cart_obj.products.count()
            }
            return JsonResponse(json_data, status=200) # HttpResponse
            # return JsonResponse({"message": "Error 400"}, status=400) # Django Rest Framework
    return redirect("cart:home")

# remote item from cart
def remove_from_cart(request, slug):
    cart_id = request.session.get("cart_id", None)                      # Get Cart_id from request
    item = get_object_or_404(CartItem, item=slug)                       # Get item from CartItem  
    order_qs = Cart.objects.filter(                                     # Get Cart_object
        id=cart_id,
    )
    if order_qs.exists():                                               # Check if Cart_obj is available
        order = order_qs[0]                                             # Get Cart details
        order_items =order.items.all()                                  # Get all the items in CartItem
        if item in order_items:                                         # Check if item is in CartItem            
            order.items.remove(item)                                    # Remote item from Cart          
            request.session['cart_items'] -= item.quantity              # Update 'cart_items' attribute
            CartItem.objects.filter(item=slug,cartid=cart_id).delete()  # Delete item from CartItem
            return redirect("cart:home")
        else:
            return redirect("cart:home")
    else:
        return redirect("cart:home")    

def remove_single_item_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
            messages.info(request, "This item quantity was updated.")
            return redirect("core:order-summary")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("core:product", slug=slug)
    else:
        messages.info(request, "You do not have an active order")
        return redirect("core:product", slug=slug)        

def checkout_home(request):
    cart_obj, cart_created = Cart.objects.new_or_get(request)
    order_obj = None
    if cart_created or cart_obj.products.count() == 0:
        return redirect("cart:home")
    login_form = LoginForm()
    guest_form = GuestForm()
    address_form = AddressForm()
    billing_address_id = request.session.get("billing_address_id", None)
    shipping_address_id = request.session.get("shipping_address_id", None)
    billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
    address_qs = None
    if billing_profile is not None:
        order_obj, order_obj_created = Order.objects.new_or_get(billing_profile, cart_obj)
        if request.user.is_authenticated:
            address_qs = Address.objects.filter(billing_profile=billing_profile)
        if shipping_address_id:
            order_obj.shipping_address = Address.objects.get(id=shipping_address_id)
            del request.session["shipping_address_id"]
        if billing_address_id:
            order_obj.billing_address = Address.objects.get(id=billing_address_id)
            del request.session["billing_address_id"]
        if billing_address_id or shipping_address_id:
            order_obj.save()
    if request.method == "POST":
        is_done = order_obj.check_done()
        if is_done:
            order_obj.mark_paid()
            del request.session['cart_id']
            request.session['cart_items'] = 0
            return redirect("/cart/checkout/success/")
        # if order_qs.count() == 1:
        #     order_obj = order_qs.first()
        # else:
        #     order_obj = Order.objects.create(billing_profile=billing_profile, cart=cart_obj)

    # login_form = LoginForm(request=request)
    # guest_form = GuestForm(request=request)
    # address_form = AddressCheckoutForm()
    # billing_address_id = request.session.get("billing_address_id", None)

    # shipping_address_required = not cart_obj.is_digital


    # shipping_address_id = request.session.get("shipping_address_id", None)

    # billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
    # address_qs = None
    # has_card = False
    # if billing_profile is not None:
    #     if request.user.is_authenticated():
    #         address_qs = Address.objects.filter(billing_profile=billing_profile)
    #     order_obj, order_obj_created = Order.objects.new_or_get(billing_profile, cart_obj)
    #     if shipping_address_id:
    #         order_obj.shipping_address = Address.objects.get(id=shipping_address_id)
    #         del request.session["shipping_address_id"]
    #     if billing_address_id:
    #         order_obj.billing_address = Address.objects.get(id=billing_address_id)
    #         del request.session["billing_address_id"]
    #     if billing_address_id or shipping_address_id:
    #         order_obj.save()
    #     has_card = billing_profile.has_card

    # if request.method == "POST":
    #     "check that order is done"
    #     is_prepared = order_obj.check_done()
    #     if is_prepared:
    #         did_charge, crg_msg = billing_profile.charge(order_obj)
    #         if did_charge:
    #             order_obj.mark_paid() # sort a signal for us
    #             request.session['cart_items'] = 0
    #             del request.session['cart_id']
    #             if not billing_profile.user:
    #                 '''
    #                 is this the best spot?
    #                 '''
    #                 billing_profile.set_cards_inactive()
    #             return redirect("cart:success")
    #         else:
    #             print(crg_msg)
    #             return redirect("cart:checkout")


    context = {
        "object": order_obj,
        "billing_profile": billing_profile,
        "login_form": login_form,
        "guest_form": guest_form,
        "address_form": address_form,
        "address_qs": address_qs,
        # "has_card": has_card,
        # "publish_key": STRIPE_PUB_KEY,
        # "shipping_address_required": shipping_address_required,
    }
    return render(request, "carts/checkout.html", context)



def checkout_done_view(request):
    return render(request, "carts/checkout-done.html", {})
