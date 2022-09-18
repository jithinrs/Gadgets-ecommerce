from django.urls import path
from .views import *


urlpatterns = [
    path("product/",product_list,name='product'),
    path("add_product",add_product,name='add_product'),
    path("product_delete/<int:id>",product_delete,name='product_delete'),
    path("product_update/<int:id>",update_produect,name='product_update'),
]