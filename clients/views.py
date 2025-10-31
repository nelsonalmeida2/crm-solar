# clients/views.py

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from .models import Company

# Importar modelos de outras apps (para buscar dados relacionados)
from energy.models import CPE
from sales.models import Opportunity


@login_required
def company_list_view(request):
    """ Exibe a lista completa de clientes (Companies) para navegação. """
    companies = Company.objects.all().order_by('name')
    return render(request, 'clients/company_list.html', {'companies': companies})


@login_required
def company_detail_view(request, pk):
    """ Exibe o detalhe de uma empresa, agregando CPEs e Oportunidades. """

    # 1. Obter a entidade principal (PK é o NIF/CharField)
    company = get_object_or_404(Company, pk=pk)

    # 2. Buscar Dados Relacionados Otimizados (de outros módulos)
    # Estas consultas são possíveis graças aos related_names definidos nos modelos
    cpes = company.cpes.all().select_related('address', 'provider')
    opportunities = company.opportunities.all().select_related('opportunity_status', 'product')

    context = {
        'company': company,
        'cpes': cpes,
        'opportunities': opportunities,
    }

    # O template será clients/templates/clients/company_detail.html
    return render(request, 'clients/company_detail.html', context)