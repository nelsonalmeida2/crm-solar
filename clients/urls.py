# clients/urls.py

from django.urls import path
from . import views

app_name = 'clients'

urlpatterns = [
    path('', views.company_list_view, name='company_list'),

    path('<str:pk>/', views.company_detail_view, name='company_detail'),
]