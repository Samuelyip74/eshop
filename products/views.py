from django.views.generic import ListView, DetailView
from django.shortcuts import render

from carts.models import Cart
from .models import Product
# Create your views here.

class ProductFeaturedListView(ListView):
    template_name = "products/list.html"


    def get_queryset(self, *args, **kwargs):
        request = self.request
        return Product.objects.featured()


class ProductFeaturedDetailView(DetailView):
    queryset = Product.objects.featured()
    template_name = "products/featured-detail.html"

    # def get_queryset(self, *args, **kwargs):
    #     request = self.request
    #     return Product.objects.featured()

class ProductListView(ListView):
    #queryset = Product.objects.all()
    template = "products/product_list.html"

    def get_context_data(self, *args, **kwargs):
            context = super(ProductListView, self).get_context_data(*args, **kwargs)
            print(context)
            cart_obj, new_obj = Cart.objects.new_or_get(self.request)
            context['cart'] = cart_obj
            return context

    def get_queryset(self, *args, **kwargs):
        request = self.request
        return Product.objects.all()

class ProductDetailSlugView(DetailView):
    #queryset = Product.objects.all()
    template_name = "products/product_detail.html"

    def get_context_data(self, *args, **kwargs):
        context = super(ProductDetailSlugView, self).get_context_data(*args, **kwargs)
        cart_obj, new_obj = Cart.objects.new_or_get(self.request)
        context['cart'] = cart_obj
        return context

    '''
    get_object query the item in the database, and raise exception if not found
    '''
    def get_object(self, *args, **kwargs):
        request = self.request
        slug = self.kwargs.get('slug')

        try:
            instance = Product.objects.get(slug=slug, active=True)
        except Product.DoesNotExist:
            raise Http404("Not found..")
        except Product.MultipleObjectsReturned:
            qs = Product.objects.filter(slug=slug, active=True)
            instance = qs.first()
        except:
            raise Http404("Error ")
        instance.viewed += 1
        instance.save()
        return instance