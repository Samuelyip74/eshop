import random
import os
import math
from django.conf import settings

from django.db import models
from django.db.models import Q
from django.db.models.signals import pre_save
from django.urls import reverse
from eshop.utils import unique_slug_generator

User = settings.AUTH_USER_MODEL

def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext

def upload_image_path(instance, filename):
    # print(instance)
    #print(filename)
    new_filename = random.randint(1,3910209312)
    name, ext = get_filename_ext(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
    return "products/{new_filename}/{final_filename}".format(
            new_filename=new_filename, 
            final_filename=final_filename
            )

class ProductQuerySet(models.query.QuerySet):
    def active(self):
        return self.filter(active=True)

    def featured(self):
        return self.filter(featured=True, active=True)

    def search(self, query):
        lookups = (Q(title__icontains=query) | 
                  Q(description__icontains=query) |
                  Q(price__icontains=query) |
                  Q(tag__title__icontains=query)
                  )
        # tshirt, t-shirt, t shirt, red, green, blue,
        return self.filter(lookups).distinct()

class ProductManager(models.Manager):
    def get_queryset(self):
        return ProductQuerySet(self.model, using=self._db)

    def all(self):
        return self.get_queryset().active()

    def featured(self): #Product.objects.featured() 
        return self.get_queryset().featured()

    def get_by_id(self, id):
        qs = self.get_queryset().filter(id=id) # Product.objects == self.get_queryset()
        if qs.count() == 1:
            return qs.first()
        return None

    def search(self, query):
        return self.get_queryset().active().search(query)

# Create your models here.
class Product(models.Model):
    user            = models.ForeignKey(User, null=True, blank=True, on_delete='CASCADE')
    title           = models.CharField(max_length=120)
    slug            = models.SlugField(blank=True, unique=True)
    shortdesc       = models.CharField(max_length=120,null=True, blank=True,)
    description     = models.TextField()
    price           = models.DecimalField(decimal_places=2, max_digits=20, default=0.00)
    discountedprice = models.DecimalField(decimal_places=2, max_digits=20, default=0.00)
    image           = models.ImageField(upload_to=upload_image_path, null=True, blank=True)
    featured        = models.BooleanField(default=False)
    active          = models.BooleanField(default=True)
    timestamp       = models.DateTimeField(auto_now_add=True)
    is_digital      = models.BooleanField(default=False) # User Library
    viewed          = models.IntegerField(default=0,null=True, blank=True) # User Library


    objects = ProductManager()

    def get_absolute_url(self):
        #return "/products/{slug}/".format(slug=self.slug)
        return reverse("products:detail", kwargs={"slug": self.slug})

    def __str__(self):
        return self.title

    def __unicode__(self):
        return self.title

    @property
    def name(self):
        return self.title

    def get_downloads(self):
        qs = self.productfile_set.all()
        return qs

    def get_discount(self):
        return 100 - math.ceil(self.discountedprice / self.price * 100)

def product_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(product_pre_save_receiver, sender=Product) 


class Imagep(models.Model):
    product = models.ForeignKey(Product, default=None, on_delete='CASCADE')
    image   = models.ImageField(upload_to=upload_image_path, null=True, blank=True)

    def __str__(self):
        return f"{self.image} of {self.product}"
