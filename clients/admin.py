# clients/admin.py

from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from .models import Company, Contact, CompanyGroup
from core.models import Observation # Para Inlines, se necessário

# ----------------------------------------------------------------------
# 1. INLINES (Opcional, mas útil para M2M ou FKs reversas)
# ----------------------------------------------------------------------

# Exemplo de Inline para Contactos na Companhia (M2M)
class CompanyContactInline(admin.TabularInline):
    model = Company.contacts.through
    extra = 1

# ----------------------------------------------------------------------
# 2. ADMIN CLASSES
# ----------------------------------------------------------------------

@admin.register(Contact)
class ContactAdmin(SimpleHistoryAdmin):
    list_display = (
        'id', 'name', 'role', 'phone', 'email',
        'preferred_contact_method', 'is_primary', 'is_active',
    )
    search_fields = ('name', 'email', 'phone')
    list_filter = (
        'is_primary', 'is_active', 'preferred_contact_method',
    )
    raw_id_fields = ('created_by', 'updated_by', 'assigned_to')


@admin.register(Company)
class CompanyAdmin(SimpleHistoryAdmin):
    list_display = ('nif', 'name', 'segment', 'email', 'has_solar_panels', 'is_hidden')
    search_fields = ('name', 'nif', 'email')
    list_filter = ('segment', 'has_solar_panels', 'is_hidden')
    raw_id_fields = ('address', 'segment', 'type_of_building', 'group', 'created_by', 'updated_by', 'assigned_to')
    # Inlines:
    inlines = [CompanyContactInline]


@admin.register(CompanyGroup)
class CompanyGroupAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'segment')
    search_fields = ('name',)
    list_filter = ('segment',)
    raw_id_fields = ('segment',)