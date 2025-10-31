# crm_solar_root/urls.py - FICHEIRO RAIZ

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # INCLUSÃO CRÍTICA: O path vazio ('') aponta para o core/urls.py,
    # que por sua vez define o 'index', 'login', 'logout' e o dashboard.
    path('', include('core.urls')),

    # Incluir outras apps (se tiver rotas específicas que não sejam o index/login)
    path('clients/', include('clients.urls')),
    path('energy/', include('energy.urls')),
    path('sales/', include('sales.urls')),
]