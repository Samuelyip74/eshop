from django.conf.urls import url
from django.urls import path,include
from .views import login_page

app_name = 'accounts'

urlpatterns = [
    url(r'^login/$', login_page, name='login'),
]