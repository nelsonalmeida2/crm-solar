# energy/urls.py

from django.urls import path
from . import views

# A variável 'urlpatterns' DEVE SER UMA LISTA
urlpatterns = [
    # path('list/', views.client_list_view, name='client_list'),
    # Adicione as rotas específicas da sua app Clients aqui
]

# Nota: Se tiver a 'client_list_view' definida no clients/views.py,
# deve incluí-la aqui. Se não tiver views específicas ainda,
# mantenha apenas a lista vazia.