# core/views.py

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
# Importa todos os modelos necessários
from sales.models import Opportunity
from clients.models import Company
from energy.models import CPE


# === 1. LÓGICA DE AUTENTICAÇÃO (MANTIDA NO CORE) ===

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            if request.session.session_key is None:
                request.session.create()
            request.session.save()
            return redirect('sales_dashboard')
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'core/login.html')


def logout_view(request):
    logout(request)
    # Redireciona para a página de login após o logout
    return redirect('login')


# === 2. DASHBOARD DE VENDAS AGREGADO ===

@login_required
def sales_dashboard_view(request):
    """
    Dashboard do Vendedor: Agrega Clientes, Pontos de Energia e Oportunidades
    atribuídos diretamente ao utilizador logado (via campo 'assigned_to').
    """
    user = request.user

    # 1. Clientes (Empresas) diretamente atribuídos
    assigned_companies = Company.objects.filter(
        assigned_to=user
    ).order_by('-updated_at')

    # 2. Pontos de Energia (CPE) diretamente atribuídos
    assigned_cpes = CPE.objects.filter(
        assigned_to=user
    ).select_related('company', 'address').order_by('-updated_at')

    # 3. Oportunidades diretamente atribuídas
    # O filtro 'assigned_to' é herdado do TimeStampedUserModel
    assigned_opportunities = Opportunity.objects.filter(
        assigned_to=user
    ).select_related(
        'company',
        'cpe',
        'opportunity_status'
    ).prefetch_related(
        'tasks'
    ).order_by('-updated_at')

    # === CÁLCULOS E CONTEXTO ===
    total_pipeline_value = sum(
        opp.opportunity_value
        for opp in assigned_opportunities
        if opp.opportunity_value is not None
    )

    context = {
        'assigned_companies': assigned_companies,
        'assigned_cpes': assigned_cpes,
        'assigned_opportunities': assigned_opportunities,

        'total_pipeline_value': total_pipeline_value,
        'open_opportunities_count': assigned_opportunities.count(),
        'user_role': 'Vendedor',
    }

    # Template a ser criado em core/templates/core/sales_dashboard.html
    return render(request, 'sales/sales_dashboard.html', context)