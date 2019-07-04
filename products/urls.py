from django.conf.urls import url
from django.urls import path

from products.views import (
    ProductListView,
    ProductDetailSlugView,
    ProductFeaturedListView,
    ProductFeaturedDetailView,
)

app_name = 'products'

urlpatterns = [
    url(r'^(?P<slug>[\w-]+)/$', ProductDetailSlugView.as_view(), name='detail'),
    url(r'^$',ProductListView.as_view(), name='list'),
]

