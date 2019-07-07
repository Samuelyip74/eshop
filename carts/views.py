from django.shortcuts import render,redirect
from products.models import Product
from .models import Cart


def cart_home(request):
    cart_obj, new_obj = Cart.objects.new_or_get(request)

    return render(request,'carts/home.html',{})

def cart_update(request):
    # product_id = 1
    # product_obj = Product.objects.get(id=product_id)
    # cart_obj, new_obj = Cart.objects.new_or_get(request)
    # cart_obj.products.add(product_obj)
    # return redirect("cart:home")

    product_id = request.POST.get('product_id')
    
    if product_id is not None:
        try:
            product_obj = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            print("Show message to user, product is gone?")
            return redirect("cart:home")
        cart_obj, new_obj = Cart.objects.new_or_get(request)
        if product_obj in cart_obj.products.all():
            cart_obj.products.remove(product_obj)
            added = False
        else:
            cart_obj.products.add(product_obj) # cart_obj.products.add(product_id)
            added = True
        request.session['cart_items'] = cart_obj.products.count()
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
