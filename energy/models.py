# energy/models.py

from django.db import models
from core.models import TimeStampedUserModel, Address, Provider, BuildingType  # Importa do core
from clients.models import Company  # Importa de clients


class CPE(TimeStampedUserModel):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=100, unique=True, verbose_name="CPE/CUI Code")

    # Relações com outras apps:
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True, blank=True, related_name='cpes')
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, blank=True)
    provider = models.ForeignKey(Provider, on_delete=models.SET_NULL, null=True, blank=True)
    type_of_building = models.ForeignKey(BuildingType, on_delete=models.SET_NULL, null=True, blank=True)

    # Dados técnicos:
    tension = models.CharField(max_length=50, null=True, blank=True)
    # Assumindo que contracted_power é um float para manter fiel ao original
    contracted_power = models.FloatField(null=True, blank=True, verbose_name="Contracted Power (kVA)")
    consumption = models.FloatField(null=True, blank=True, help_text="Estimated or Average Annual Consumption (kWh)")
    fidelization_end_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=False)
    has_solar_panels = models.BooleanField(default=False)

    def __str__(self):
        return self.code