# energy/admin.py

from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from .models import CPE


@admin.register(CPE)
class CPEAdmin(SimpleHistoryAdmin):
    # 1. Adicionar campos de auditoria ao list_display
    list_display = (
        'id',
        'code',
        'company',
        'provider',
        'contracted_power',
        'has_solar_panels',
        'is_active',
        # CAMPOS ADICIONADOS PARA VISUALIZAÇÃO
        'assigned_to',
        'created_by',
        'updated_at',
    )
    search_fields = ('code', 'company__name')
    list_filter = ('provider', 'has_solar_panels', 'is_active', 'type_of_building')

    # Adicionar os campos de auditoria/atribuição ao raw_id_fields
    raw_id_fields = ('company', 'address', 'provider', 'type_of_building', 'created_by', 'updated_by', 'assigned_to')

    fieldsets = (
        ("General Info", {
            'fields': ('company', 'code', 'address', 'provider', 'is_active', 'has_solar_panels')
        }),
        ("Technical Specs", {
            'fields': ('tension', 'contracted_power', 'consumption', 'type_of_building', 'fidelization_end_date')
        }),
        # 2. NOVO FIELDSET para os campos de auditoria/atribuição
        ("CRM Ownership", {
            # created_by e updated_by são apenas de leitura, mas assigned_to pode ser editado
            'fields': ('assigned_to', 'created_by', 'updated_by')
        }),
    )

    # 3. OTIMIZAÇÃO: Preencher created_by e updated_by automaticamente
    def save_model(self, request, obj, form, change):
        if not obj.pk:
            # Apenas preenche created_by na primeira criação
            obj.created_by = request.user

        # updated_by é sempre o último utilizador que guardou
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)

    # Opcional: Impedir a edição manual do created_by/updated_by no formulário de edição
    def get_readonly_fields(self, request, obj=None):
        fields = super().get_readonly_fields(request, obj)
        if obj:  # Se for uma edição (não criação)
            fields += ('created_by',)
        return fields