from django.views.generic import ListView, DetailView
from django.shortcuts import render

from .models import Product
# Create your views here.

class ProductListView(ListView):
    queryset = Product.objects.all()
    template = "products/product_list.html"

def get_context_data(self, *args, **kwargs):
        context = super(ProductListView, self).get_context_data(*args, **kwargs)
        print(context)
        #cart_obj, new_obj = Cart.objects.new_or_get(self.request)
        #context['cart'] = cart_obj
        return context

def get_queryset(self, *args, **kwargs):
    request = self.request
    return Product.objects.all()

class ProductDetailSlugView(DetailView):
    queryset = Product.objects.all()
    template_name = "products/product_detail.html"

    def get_context_data(self, *args, **kwargs):
        context = super(ProductDetailSlugView, self).get_context_data(*args, **kwargs)
        #cart_obj, new_obj = Cart.objects.new_or_get(self.request)
        #context['cart'] = cart_obj
        return context

    def get_object(self, *args, **kwargs):
        request = self.request
        slug = self.kwargs.get('slug')

        #instance = get_object_or_404(Product, slug=slug, active=True)
        try:
            instance = Product.objects.get(slug=slug, active=True)
        except Product.DoesNotExist:
            raise Http404("Not found..")
        except Product.MultipleObjectsReturned:
            qs = Product.objects.filter(slug=slug, active=True)
            instance = qs.first()
        except:
            raise Http404("Uhhmmm ")
        return instance