# crm_solar_root/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('clients/', include('clients.urls', namespace='clients')),
    path('energy/', include('energy.urls')),
    path('sales/', include('sales.urls')),
]