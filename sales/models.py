# sales/models.py

from django.db import models
from core.models import TimeStampedUserModel, Product  # Importa do core
from clients.models import Company  # Importa de clients
from energy.models import CPE  # Importa de energy


class OpportunityStatus(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)  # E.g., Lead, Proposal Sent, Won, Lost

    def __str__(self):
        return self.name


class Opportunity(TimeStampedUserModel):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)

    # Relações com outras apps:
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True, blank=True, related_name='opportunities')
    cpe = models.ForeignKey(CPE, on_delete=models.SET_NULL, null=True, blank=True)  # Liga à instalação de energia

    # Relações dentro desta APP
    opportunity_status = models.ForeignKey(OpportunityStatus, on_delete=models.SET_NULL, null=True)

    # Relações com o módulo CORE
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)

    # Campos da oportunidade:
    opportunity_value = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Estimated value of the opportunity"
    )
    revenue = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Actual revenue if the opportunity is closed"
    )
    description = models.TextField(null=True, blank=True)
    closed_at = models.DateTimeField(null=True, blank=True)
    exclusivity_expires_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name