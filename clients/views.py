# clients/views.py

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Company 

@login_required
def client_list_view(request):
    """ Mostra a lista completa de clientes (Companies). """
    companies = Company.objects.all()
    return render(request, 'crmsolar/client_list.html', {'companies': companies})