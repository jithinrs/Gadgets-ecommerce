from django.urls import path
from .import views


urlpatterns = [
    path('signup',views.Register,name='signup'),
    path('login',views.Login,name='login'),
    path('logout',views.Logout,name='logout'),
    path('verify/', views.verify_code ,name='verify'),
    path('user_profile',views.user_profile,name='user_profile'),
    path('user_profile_update',views.user_profile_update,name='user_profile_update'),
]