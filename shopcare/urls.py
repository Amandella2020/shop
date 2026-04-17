from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('shopapi/', include('shop.urls')),  # includes all your app endpoints
]