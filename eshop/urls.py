"""eshop URL Configuration


"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.conf.urls import url
from django.urls import path,include

from .views import home

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^products/',include('products.urls')),
    url(r'^cart/',include('carts.urls')),
    url(r'^$',home, name='homepage'),
]

if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
