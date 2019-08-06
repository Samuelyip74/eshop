
from django.conf.urls import url
from django.urls import path,include

from .views import (
    cart_home, 
    cart_update,
    checkout_home,
    checkout_done_view,
    remove_from_cart,
    remove_single_item_from_cart,
)


app_name = 'cart'

urlpatterns = [
    url(r'^$', cart_home, name='home'),
    url(r'^checkout/success/$', checkout_done_view, name='success'),
    url(r'^checkout/$', checkout_home, name='checkout'),
    url(r'^update/$', cart_update, name='update'),
    path('remove-from-cart/<slug>/', remove_from_cart, name='remove-from-cart'),
    path('remove-item-from-cart/<slug>/', remove_single_item_from_cart,
         name='remove-single-item-from-cart'),
]