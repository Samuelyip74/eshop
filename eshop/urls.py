from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.conf.urls import url
from django.urls import path,include
from django.contrib.auth.views import LogoutView
from django.views.generic import TemplateView, RedirectView


from .views import home

urlpatterns = [
    path('admin/', admin.site.urls),
    #url(r'^accounts/login/$', RedirectView.as_view(url='/login')),
    url(r'^accounts/', include("accounts.urls", namespace='account')),
    # url(r'^account/', include("accounts.urls", namespace='account')),
    # url(r'^accounts/', include("accounts.passwords.urls")),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(r'^products/',include('products.urls')),
    url(r'^cart/',include('carts.urls')),
    url(r'^$',home, name='homepage'),
]

if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
