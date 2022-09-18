from django.urls import path
from .views import *
urlpatterns = [
 path('place_order/',place_order,name = 'place_order'),
 path('payments/',payments,name = 'payments'),
 path('payments_completed/',payments_completed,name = 'payments_completed'),
 path('user_orders',user_orders,name="user_orders"),
 path('admin_orders',admin_orders_list,name="admin_orders"),

]