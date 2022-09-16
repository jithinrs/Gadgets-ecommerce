from django.urls import path
from .views import *
urlpatterns = [
 path('place_order/',place_order,name = 'place_order'),
 path('payments/',payments,name = 'payments'),
 path('payments_completed/',payments_completed,name = 'payments_completed')
]