# sales/admin.py

from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from .models import OpportunityStatus, Opportunity
from core.models import Observation, Task  # Para inlines


# ----------------------------------------------------------------------
# 1. INLINES (Opcional, para anexar Tasks e Observations diretamente na Opportunity)
# ----------------------------------------------------------------------

class OpportunityTaskInline(admin.TabularInline):
    # A Task é importada do módulo core
    model = Task
    extra = 1
    raw_id_fields = ('opportunity', 'company', 'contact', 'task_type', 'created_by', 'updated_by', 'assigned_to')


class OpportunityObservationInline(admin.TabularInline):
    # A Observation é importada do módulo core
    model = Observation
    extra = 1
    raw_id_fields = ('task', 'company', 'group', 'contact', 'cpe', 'opportunity')


# ----------------------------------------------------------------------
# 2. ADMIN CLASSES
# ----------------------------------------------------------------------

@admin.register(OpportunityStatus)
class OpportunityStatusAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(Opportunity)
class OpportunityAdmin(SimpleHistoryAdmin):
    list_display = (
        'id', 'name', 'company', 'cpe', 'opportunity_status',
        'opportunity_value', 'revenue', 'closed_at'
    )
    search_fields = ('name', 'company__name')
    list_filter = ('opportunity_status', 'product', 'closed_at')
    # Adiciona raw_id_fields para FKs de outras apps:
    raw_id_fields = ('cpe', 'company', 'product', 'opportunity_status', 'created_by', 'updated_by', 'assigned_to')

    # Inlines para Tasks e Observações:
    inlines = [OpportunityTaskInline, OpportunityObservationInline]