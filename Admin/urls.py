from django.urls import path
from .views import *
urlpatterns = [
    path("admin_login",Admin_login,name='admin_login'),
    path("admin_page",Admin_page,name='admin_page'),
    path("logout",Admin_logout,name='admin_logout'),
    path("user_display",user_display,name='user_display'),
    path("user_block/<int:id>/<int:flag>",user_block,name='user_block'),
]