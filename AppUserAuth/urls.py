from django.contrib import admin
from django.urls import path
from AppUserAuth import views
from AppAdmin import views 


urlpatterns = [
     
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('home/', views.home, name='home'),
    path('logout',views.logout,name='logout'),
    
   
]
