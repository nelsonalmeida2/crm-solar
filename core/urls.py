# core/urls.py - CRIAR ESTE FICHEIRO

from django.urls import path
from . import views
from .views import login_view, logout_view, sales_dashboard_view  # As views estão em core/views.py

urlpatterns = [
    # A rota principal ('') e 'sales_dashboard' apontam para o Dashboard
    path('dashboard/sales/', views.sales_dashboard_view, name='sales_dashboard'),
    path('', views.sales_dashboard_view, name='index'),
    # Rotas de Autenticação (Tratadas aqui)
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Se mantiver a client_list_view em clients/views.py, não a ligue aqui,
    # ela será ligada através do clients/urls.py incluído no root.
]