from django.urls import path, include
from myproject.blog.apis.product import ProductAPI


urlpatterns = [
    path('product/', ProductAPI.as_view(), name='product'),
]

