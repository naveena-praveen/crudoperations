
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('',include('AppAdmin.urls')),
    path('',include('AppUserAuth.urls')),
    path('admin/', admin.site.urls),
    
]
