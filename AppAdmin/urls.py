from django.contrib import admin
from django.urls import path
from AppUserAuth import views
from . import views


urlpatterns = [
    
     path('adminhome/', views.admin_home, name='admin_home'), 
     path('admin1/', views.admin_login, name='admin_login'),
     path('',views.user_display,name='user_display'),
     path('adminlogout/',views.admin_logout,name='admin_logout'),
     path('',views.admin_panel,name='admin_panel'),
     # delete view 
     path('delete_user/<int:user_id>/', views.delete_user, name='delete_user'),
     path('user/update/<int:user_id>/', views.user_update, name='user_update'),
     path('user/add/', views.add_user, name='add_user'),
   
]
