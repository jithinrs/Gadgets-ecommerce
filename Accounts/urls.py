from django.urls import path
from .import views


urlpatterns = [
    path('signup',views.Register,name='signup'),
    path('login',views.Login,name='login'),
    path('logout',views.Logout,name='logout'),
    path('verify/', views.verify_code ,name='verify'),
    path('user_dashbord',views.user_dashbord,name='user_dashbord'),
    path('account_detail',views.account_detail,name='account_detail'),
    path('account_detail_update',views.account_detail_update,name='account_detail_update'),
    path('addresses',views.addresses,name='addresses'),
]